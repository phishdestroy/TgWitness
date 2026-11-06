# Những nội dung đã được kiểm thử

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/

Thử nghiệm Telegram trực tiếp, các kiểm tra tự động, kiểm tra trên trình duyệt và những nội dung vẫn chưa được xác minh.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bằng chứng và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/)

![Bằng chứng & xác minh](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Cập nhật ngày 6 tháng 11 năm 2026.** Kết quả gắn liền với phiên bản, môi trường và tải công việc được ghi lại cho mỗi lần chạy. [Các tính năng hiện tại](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) mô tả các luồng công việc có sẵn; trang này ghi lại những gì đã thực sự được kiểm tra.

[Biểu đồ hiệu suất](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Bản kiểm toán tiếng Anh đã được ký tên](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Các số liệu có thể tải xuống](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Bằng chứng mới nhất | Kết quả | Phạm vi |
| --- | --- | --- |
| Kiểm toán phiên bản · 6/11 | Các bài kiểm tra lõi 1,461 đã vượt qua; các bài kiểm tra nền tảng 37 bị bỏ qua | Nguồn `92e539af40d8`; các phát hiện mở được giữ nguyên |
| Dữ liệu xuất mới · 6/11 | 127.713 và 141.781 bản ghi/giây, chu kỳ hoàn chỉnh | Hai tài khoản trên mỗi máy chủ; văn bản và siêu dữ liệu được truyền qua WARP |
| Lưu trữ đã được giữ lại · 6/11 | Tệp lưu trữ 48; bản ghi 3,598,381 đã được xác minh | Các kho lưu trữ hiện có đã được kiểm tra so với các khóa không gian làm việc được ghim |
| Trusted Live · 5/11 | Ghi lại hoạt động CPU được bảo vệ và kiểm tra WARP | Đăng nhập trên máy tính để bàn chính thức và tính năng xuất dữ liệu gốc vẫn chưa được xác nhận |
| Phala / Intel TDX · 4/11 | Tất cả các kiểm tra của trình xác minh 16 đều đã vượt qua trong các lần chạy sau đó | Triển khai trước đây; không có tài khoản Telegram trên CVM |

**Trên trang này**

- [Kiểm toán bản phát hành và các bản xuất mới · 6 tháng 11 năm 2026](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu và WARP · 5 tháng 11 năm 2026](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Triển khai Phala Cloud trực tiếp · 4 tháng 11 năm 2026](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Danh mục nhật ký máy chủ trực tiếp · 1 tháng 11 năm 2026](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Các kiểm tra ngoại tuyến và kiểm tra tiêm lỗi gần đây · 1 tháng 11 năm 2026](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Thử nghiệm Telegram trực tiếp, toàn bộ tài khoản · 29 tháng 10 năm 2026](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Tệp xuất được bảo vệ bằng mật khẩu, mở bằng libarchive · 29 tháng 10 năm 2026](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Thử nghiệm Telegram trực tiếp · Từ ngày 27 đến 29 tháng 10 năm 2026](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Đo lường dung lượng cục bộ tổng hợp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Tìm kiếm toàn văn trên một triệu tin nhắn · 5 tháng 11 năm 2026](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Điều kiện còn lại](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/#remaining-qualification)

## Kiểm toán bản phát hành và các bản xuất mới · 6 tháng 11 năm 2026

Cuộc kiểm toán đã sử dụng phiên bản v0.9.1 tại nguồn `92e539af40d8368d198ff5e040f1d876f2c1310e`, bản phát hành `92e539af40d8-83e41104669e`. Các kiểm tra sơ bộ gói đã cài đặt đã vượt qua trên ba máy chủ. Báo cáo đã ký giữ nguyên trạng thái được quan sát tại thời điểm đó.

[![Tỷ lệ thu thập và xuất hoàn chỉnh cho hai khối lượng công việc mới](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Khối lượng công việc | Ghi lại | Thu thập | Hoàn thành chu trình | Tỷ lệ hoàn thành chu kỳ |
| --- | --- | --- | --- | --- |
| Máy chủ A · hai tài khoản | 27,030 | 189.043 s | 211.647 s | 127.713 bản ghi/giây |
| Máy chủ B · hai tài khoản | 29,299 | 182.513 s | 206.650 s | 141.781 bản ghi/giây |

Cả hai lần xuất dữ liệu đều bắt đầu mà không có tính năng tiếp tục, loại trừ các tệp đính kèm và ảnh đại diện, và kết thúc với không có bản ghi trùng lặp hoặc được tái sử dụng nào. Chu trình hoàn chỉnh bao gồm chuẩn bị, thu thập, lựa chọn, đóng gói và xác minh kho lưu trữ. Máy chủ A cũng đã thực hiện kiểm tra đọc cuộc trò chuyện được bảo vệ. Bốn sự kiện FloodWait trên máy chủ A và ba sự kiện trên máy chủ B đã được tuân thủ. Các quan sát này không xác lập một đảm bảo thông lượng chung.

| Kiểm tra | Kết quả | Yêu cầu |
| --- | --- | --- |
| Lõi pytest | Đã vượt qua 1,461 | Nền tảng 37 bỏ qua |
| Trình duyệt / trải nghiệm người dùng trình duyệt / bằng chứng / trang web | 102 / 66 / 15 / 9 đã vượt qua | Các chương trình này trùng lặp với các thử nghiệm khác; số lượng không được cộng dồn |
| Tiện ích mở rộng Capture | Đã vượt qua 124 | Ba kiểm tra Web chính thức bị chặn bởi hộp cát Chromium bắt buộc |
| Ủy quyền API | Các tuyến 269; các yêu cầu 538 đã được xử lý | Thiếu thông tin đăng nhập và quyền truy cập bị thu hồi |
| Các kho lưu trữ được giữ lại | 48/48 đã được xác minh | Bản ghi 3,598,381; khóa không gian làm việc được ghim |
| Kiểm tra trạng thái trực tuyến của đội tàu | 24/40 hồ sơ đã vượt qua | Các tuyến WARP 16 không đạt tiêu chuẩn; các cấu hình đó không được kết nối |

Báo cáo [đã ký](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) ghi lại tất cả các phát hiện còn mở, bao gồm ba lỗi trong một bản chụp nhanh cuộc trò chuyện bí mật chưa được công bố, không có trong bản dựng chính đã được kiểm toán. Báo cáo [đánh giá lịch sử công khai](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) trước đó đã sử dụng một phiên bản và khối lượng công việc khác; các tỷ lệ của báo cáo đó không được kết hợp với so sánh này.

Xác minh báo cáo gốc bằng khóa [được ghim và trình xác minh](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Chữ ký này bảo vệ báo cáo của người vận hành khỏi bị thay đổi. Đây không phải là chứng nhận độc lập, bằng chứng về quyền tác giả của Telegram hoặc chứng nhận GDPR.

## Trusted Live CPU Ubuntu và WARP · 5 tháng 11 năm 2026

Quá trình tích hợp được giữ lại đã sử dụng máy ảo Ubuntu 24.04.5 chỉ chạy trên CPU (4 vCPU, 8 GiB) trong môi trường QEMU bên trong máy chủ RunPod CPU. Bộ thu thập dữ liệu sử dụng `14e642a5`; quá trình xác minh sử dụng `02072461`. Các bản sửa lỗi cuối cùng đã được hợp nhất vào [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) dưới dạng `755f78f6`, với cây mã nguồn trùng khớp với đầu nhánh PR đã được thử nghiệm. Đây không phải là TEE.

- Một WARP Connector thực tế được báo cáo là hoạt động bình thường; HTTPS qua proxy báo cáo WARP và Gateway đã được kích hoạt. Ba lần kiểm tra đều ghi nhận cùng một địa chỉ xuất, không đảm bảo địa chỉ IP cố định.
- Việc ngắt kết nối WARP đã khiến yêu cầu qua proxy thất bại. Kết nối HTTPS trực tiếp với dịch vụ cổng đã bị từ chối. Trong không gian tên của trình ghi, các kết nối IPv4/IPv6 trực tiếp, DNS bên ngoài và bộ giải quyết UDP nhúng của Docker đã bị chặn.
- Một mã thông báo nhà cung cấp chỉ đọc có phạm vi giới hạn có thể đọc các thông tin về tình trạng hoạt động/kết nối nhưng không thể đọc mã thông báo đăng ký kết nối. Các quan sát của nhà cung cấp đã ký bao gồm các mẫu không khả dụng được chỉ định rõ ràng. Công cụ chứng kiến chạy trên máy chủ của nhà điều hành, do đó điều này chứng minh khả năng ghi lại và lưu trữ, chứ không phải việc lưu giữ bởi bên thứ ba độc lập.
- Phiên bản Desktop chính thức đã hiển thị màn hình chào mừng không cần xác thực. Dữ liệu nhập từ bàn phím được bảo vệ đã bị từ chối trong quá trình ghi lại. Ba phân đoạn hiển thị H.264 đã được giải mã và lớp phủ đồng hồ của chúng đã được kiểm tra. Tệp lưu trữ kiểm tra trước sự kiện 18 đã được xác minh dựa trên khóa ghi âm được ghim và điểm kiểm tra được lưu giữ.
- Các bài kiểm tra ghi lại cuối cùng đã vượt qua các trường hợp 114 trên CI Windows và Linux, với Chromium/FFmpeg thực tế. Năm bài kiểm tra mốc và các kiểm tra khuyến cáo về phụ thuộc đã vượt qua.

Quá trình khởi động ban đầu với cấu hình 2 vCPU/4 GiB đã hết thời gian chờ dưới tải xây dựng hình ảnh đồng thời và bị dừng bởi cơ chế bảo vệ; trường hợp này không được tính là thành công. Việc đăng nhập tài khoản thử nghiệm thủ công, xuất dữ liệu trò chuyện gốc, so sánh lai thực tế và đăng xuất từ phía Telegram vẫn chưa được thực hiện. Không có phiên Telethon nào được cung cấp được nhập vào. Các tệp đính kèm, OCR tự động, xác minh drand BLS cục bộ và chứng nhận Trusted Live TDX không đáp ứng yêu cầu.

## Triển khai trên Phala Cloud · Ngày 4 tháng 11 năm 2026

**Kết quả lịch sử: Các lần triển khai sau đó** đã vượt qua tất cả các kiểm tra xác minh 16, bao gồm Intel TDX và đường hầm nhanh. Bằng chứng khởi động lại, phát hiện địa chỉ đã ký và dấu thời gian báo cáo đã được kiểm tra riêng biệt. Mỗi CVM thử nghiệm đã được loại bỏ sau khi chạy xong.

| Cài đặt | Giá trị đã ghi lại |
| --- | --- |
| Nhà cung cấp | Phala Cloud · `tdx.small` · US-WEST-1 |
| Triển khai | `--provider phala --quick-tunnel`; không gian làm việc ban đầu trống |
| Trình thu thập ban đầu | `df7d860c` · v0.8.1 |
| Bộ thu thập với tất cả các bản sửa lỗi | `53a0f7e9` |
| Khách hàng sản xuất | `dstack-0.5.12`; Tắt quyền truy cập SSH |
| Dịch vụ bên ngoài | ntfy.sh, GitHub và Intel PCS |
| Chi phí quan sát được | Bảy CVM, tổng trị giá khoảng 1.9 cent Mỹ; giá thử nghiệm lịch sử |

Dãy sự kiện dưới đây phân biệt các lỗi ban đầu, các bản sửa lỗi và các kiểm tra đã hoàn tất. Không có tài khoản Telegram nào được kết nối với các CVM này.

**Các phiên bản triển khai 1–2 · sự khác biệt giữa các nhà cung cấp và kiểm tra hồi quy**

Hai lần triển khai đầu tiên đã phát hiện ra năm điểm khác biệt so với Phala Cloud mô phỏng. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) hiện đã tái hiện từng trường hợp này và sẽ thất bại nếu không có bản sửa lỗi tương ứng:

| Trên Phala Cloud | Trước khi khắc phục | Sửa lỗi |
| --- | --- | --- |
| Yêu cầu phải có `compose_file.name` | Lỗi HTTP 422, không tạo được gì | Cấu hình Docker Compose chứa tên CVM |
| Trừ khi được cung cấp một giá trị trống, Phala sẽ tự động thêm tập lệnh khởi động trước của riêng mình vào tệp app-compose được đo lường (phiên bản v0.0.20: thông tin đăng nhập Docker, `docker compose pull`, mật khẩu root, khóa SSH từ `user_config`) | `tdx_compose` không thành công: mã nằm ngoài cấu hình Docker Compose đã được công bố | Tệp app-compose đặt `pre_launch_script` thành `""`; Phala sau đó sẽ bỏ qua phần này |
| Nếu không có `image`, Phala sẽ chọn `dstack-dev-0.5.12`, phiên bản phát triển, với quyền truy cập SSH được kích hoạt | `server_state` không thành công. Chỉ riêng bản ghi chứng thực phần cứng là đã đạt yêu cầu trên hình ảnh này; chỉ có bản ghi nhà cung cấp và `tdx_os` mới thể hiện điều này | Quá trình triển khai yêu cầu bản dựng sản xuất của phiên bản Phala hiện tại, `dstack-0.5.12` |
| Khi cổng dstack bị tắt, thông tin chi tiết về CVM không bao giờ hiển thị mã lỗi `instance_id` | Quá trình triển khai chờ 30 phút rồi thất bại | ID phiên bản được đọc từ trạng thái CVM |
| Các thao tác khởi động lại, dừng và khởi động là các thao tác trên CVM, không phải các bản cập nhật ứng dụng | `provider_actions` không liệt kê các lần khởi động lại | Các thao tác này cũng được ghi nhận |

**Triển khai 3 · xác thực, kiểm tra quyền truy cập và bằng chứng khởi động lại**

- CVM đã chạy `dstack-0.5.12` với quyền truy cập SSH bị tắt. Bộ thu thập đã đăng địa chỉ đã ký của mình khoảng 1,5 phút sau khi được tạo. Quá trình triển khai sau đó đã thông qua `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, bản ghi chứng thực phần cứng v4, FMSPC `20a06f000000`, không ở chế độ gỡ lỗi, không thể di chuyển, hỗ trợ dữ liệu xác minh mật mã lấy từ Intel), `tdx_compose_hash`, `tdx_compose` (từng byte) và `tdx_identity` (khóa KMS).
- Bảng điều khiển tại địa chỉ trycloudflare.com trả về mã trạng thái 401 khi không có mã thông báo hoặc sử dụng mã thông báo sai, và trả về mã trạng thái 200 khi sử dụng mã thông báo của bảng điều khiển.
- `verify` với `--source` được thiết lập trỏ đến kho lưu trữ cam kết trên GitHub và dấu vân tay được truyền riêng biệt: máy chủ, `server_state`, tường lửa (không có cổng, không có điểm cuối công khai), nhật ký nhà cung cấp, báo cáo, dấu vân tay, băm nguồn, quá trình khởi động và năm kiểm tra `tdx_*` đều đạt yêu cầu. Cloudflare và `tdx_os` không khả dụng, do đó kết quả là CHƯA HOÀN THÀNH.
- Hai lần khởi động lại thông qua API của Phala: mỗi lần, CVM đều hoạt động trở lại trong vòng chưa đầy hai phút với cùng một khóa thu thập, một địa chỉ đã ký mới và địa chỉ cũ trả về mã trạng thái 530. `verify` đã báo cáo lần khởi động mới và cả hai lần khởi động lại với trạng thái REVIEW. Với `--evidence`, hệ thống đã xác nhận các chữ ký nhật ký và ba lần khởi động, mỗi lần đều có bản ghi chứng thực phần cứng Intel TDX riêng từ cùng một CVM.
- Lệnh `destroy` chỉ xóa CVM đó. Sau đó, không gian làm việc trở nên trống rỗng và địa chỉ bảng điều khiển ngừng phản hồi.
- Kết quả kiểm tra giá trên trình hướng dẫn bảng điều khiển hiển thị `tdx.small` với mức giá 0,058 USD mỗi giờ. Khi nhập sai khóa, hệ thống sẽ hiển thị thông báo đơn giản “không chấp nhận khóa API”.

**Các bản sửa lỗi tiếp theo · phát hiện địa chỉ đã ký và đo lường hệ điều hành**

- Nếu không có khóa địa chỉ, `verify` sẽ tuân theo bài đăng hợp lệ mới nhất về chủ đề địa chỉ, được in trong cấu hình Docker Compose đã công bố. Một bài đăng giả mạo đã gửi nó đến một máy chủ không tồn tại, và `statement` đã thất bại: kẻ giả mạo không thể giả danh là người thu thập, nhưng có thể ngăn chặn quá trình xác minh của bên thứ ba, trong tối đa 12 giờ bằng cách sử dụng dấu thời gian giả mạo trong tương lai. Hiện tại, bộ thu thập cũng đăng địa chỉ của mình kèm chữ ký bằng khóa riêng, `verify` chỉ chấp nhận các bài đăng như vậy khi chính bộ thu thập tạo ra chúng, và các bài đăng được sắp xếp theo thời gian nhận của ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) phát lại các bài đăng giả mạo. Một CVM chỉ chạy quy trình này từ một bản cam kết (commit) chứa nó, do đó người thu thập của lần chạy này chưa ký địa chỉ của mình và `verify` đã thông báo điều đó.
- `tdx_os` không thể chạy nếu thiếu `dstack-mr`; phiên bản hiện tại của công cụ này có lệnh `measure-os` thay vì `measure --json` được nêu trong tài liệu. Công cụ xác minh hiện tự tính MRTD và RTMR0-2 từ ảnh hệ điều hành đã công bố và cấu hình máy ảo, bao gồm các bảng ACPI.

**Triển khai 4 · tất cả các kiểm tra 16, niêm phong báo cáo và xác minh khởi động lại**

- Quá trình triển khai đã tải xuống tệp `dstack-0.5.12` đã được công bố một lần, đối chiếu nó với băm hình ảnh hệ điều hành mà CVM báo cáo, và tệp `tdx_os` đã vượt qua kiểm tra: các giá trị MRTD, RTMR0, RTMR1 và RTMR2 trùng khớp với các giá trị được tính toán cho QEMU 8.2.2, 1 vCPU và 2 GiB. Cùng một phép tính này lại cho kết quả RTMR0 khác khi đối với cấu hình được khai báo là 4 GiB, 2 vCPU, QEMU 9.2.1 hoặc có thêm thẻ mạng thứ hai, và không đạt yêu cầu khi nhân hệ điều hành, phần sụn hoặc dòng lệnh bị thay đổi cũng như đối với hình ảnh phát triển.
- `verify` đã vượt qua toàn bộ 16 bài kiểm tra, bao gồm cả bộ kết nối của đường hầm nhanh, do đó kết quả là ĐẠT. Hệ thống đã tạo ra chứng chỉ dưới dạng HTML và PDF, được niêm phong kỹ thuật số bằng chữ ký và dấu thời gian, bao gồm dấu thời gian eIDAS đủ điều kiện từ đơn vị đóng dấu thời gian TSU 202301 của Chính phủ Bỉ (tình trạng được cấp trên danh sách tin cậy của Bỉ), dấu thời gian FreeTSA và chữ ký của bên xác minh; `check-report` đã xác nhận tất cả các yếu tố này cùng với chữ ký trên tệp PDF.
- Sau khi khởi động lại, `verify --evidence` đã xác nhận hai lần khởi động, mỗi lần đều đi kèm với một chứng nhận phần cứng được tạo ra bên trong CVM và mỗi lần đều được khởi động từ `dstack-0.5.12` đã được công bố; cả lần khởi động lại và lần khởi động mới đều ở trạng thái REVIEW.
- `destroy` đã để không gian làm việc trống rỗng.

**Triển khai 5 · phát hiện có chữ ký của bộ thu thập và từ chối bài đăng giả mạo**

Trình thu thập dữ liệu đã chạy từ bản cam kết (commit) `53a0f7e9`, bao gồm các bản sửa lỗi nêu trên.

- Bộ thu thập đã đăng địa chỉ của mình được ký bằng khóa riêng, ngay bên cạnh bài đăng HMAC của nhà điều hành. Sau đó, hai bài đăng giả mạo đã được thêm vào chủ đề này, một bài có HMAC bằng 0 và một bài được ký bằng một khóa Ed25519 khác, cả hai đều tuyên bố thời gian là năm 2096. `verify` đã lấy địa chỉ được ký bằng khóa của bộ thu thập và vượt qua tất cả 16 bước kiểm tra; con dấu này một lần nữa mang dấu thời gian đủ điều kiện của Bỉ, dấu thời gian của FreeTSA và chữ ký của bên xác minh, và `check-report` đã xác nhận các thông tin này.
- Sau khi khởi động lại, bộ thu thập đã đăng địa chỉ mới đã được ký: `verify` đã phát hiện ngay lập tức, **của nhà điều hành đã tìm thấy địa chỉ hiện tại** 27 giây sau đó từ bài đăng HMAC, và cả hai đều bỏ qua các bài đăng giả mạo. `verify --evidence` đã xác nhận hai lần khởi động từ `dstack-0.5.12`.
- Quá trình triển khai đã hiển thị mức phí mà Phala tính cho CVM, bao gồm cả đĩa: 0,06078 USD mỗi giờ.

### Trình hướng dẫn bảng điều khiển và phạm vi còn lại

Trình hướng dẫn bảng điều khiển đã chạy trên Phala Cloud hai lần, một lần thông qua API công việc của nền tảng này và một lần thông qua trình duyệt sử dụng Chromium thực: kiểm tra giá, tạo cấu hình với cam kết dưới **Advanced**, cả sáu kiểm tra chứng thực đều đạt yêu cầu, danh sách máy chủ hiển thị mức giá được tính (44,37 USD mỗi tháng), **Find địa chỉ hiện tại**, quá trình tải xuống cấu hình Docker Compose đã được đo lường, và quá trình xóa. Trình duyệt không ghi nhận bất kỳ lỗi trang nào. Sau mỗi lần thực hiện, không gian làm việc đều trống rỗng.

Không bao gồm: tên miền Cloudflare trên Phala, tài khoản Telegram trên CVM và hình ảnh `dstack-0.6.1` . Giá của trình hướng dẫn trước khi tạo chỉ bao gồm giá tính toán của Phala, vì API của nó chỉ liệt kê giá đĩa cho một CVM hiện có; danh sách máy chủ hiển thị giá được tính sau khi tạo. Tất cả giá trong phần này được ghi nhận vào ngày 4 tháng 11 năm 2026.

## Danh mục nhật ký máy chủ trực tiếp · 1 tháng 11 năm 2026

Vào khoảng 19:15 UTC, các truy vấn SQLite `query_only` chỉ đọc liên tiếp đã đếm số sự kiện trong mười cơ sở dữ liệu không gian làm việc trên một máy chủ đang hoạt động. Việc thu thập dữ liệu vẫn tiếp tục trong suốt quá trình thực hiện các truy vấn, do đó đây không phải là một bản chụp nhanh nguyên tử trên các không gian làm việc.

| Được quan sát trên mười cơ sở dữ liệu không gian làm việc | Số lượng |
| --- | --- |
| Các không gian làm việc có ít nhất một sự kiện `message.new` | 8 |
| Các bản ghi nhật ký, bao gồm các sự kiện vận hành | 1,610,818 |
| Sự kiện `message.new` | 900,232 |
| Các sự kiện `message.edited` | 80,683 |
| Các sự kiện `message.deleted` | 400,536 |
| Các sự kiện `message.recovered` | 53,403 |
| Các sự kiện `message.snapshot` | 2,183 |
| Các sự kiện `media.saved` | 50,418 |
| Các sự kiện `media.failed` | 5,575 |
| Các sự kiện `coverage.gap` | 11 |
| Dung lượng cơ sở dữ liệu, không bao gồm các tệp WAL và tệp phương tiện | 7,909,003,264 |

Đây là **số lượng sự kiện**, không phải tin nhắn, người dùng hoặc tệp phương tiện duy nhất. Cùng một tin nhắn có thể xuất hiện trong nhiều không gian làm việc, và việc chỉnh sửa hoặc xóa có thể tạo ra một sự kiện nhật ký khác. `media.failed` đếm các sự kiện thất bại lịch sử, không phải hàng đợi phương tiện hiện tại. Các truy vấn **không** xác minh lại chữ ký và chuỗi băm đầy đủ của tất cả 1,610,818 bản ghi, không đo lường tỷ lệ giao hàng hoặc thông lượng, cũng như không xác nhận rằng mọi sự kiện Telegram đều được ghi lại. Không có nội dung tin nhắn, ID tài khoản hoặc ID cuộc trò chuyện, nhãn không gian làm việc, thông tin đăng nhập hoặc tệp tin riêng tư nào được công bố tại đây.

Tại thời điểm đánh giá này, bộ giám sát công khai được cấu hình riêng biệt đã bao quát ba nguồn: một phản hồi thu thập là OK và hai phản hồi báo cáo `no_response`. Bộ giám sát này không phải là bản tóm tắt tình trạng hoạt động của mười không gian làm việc. `no_response` có nghĩa là người quan sát không thể nhận được phản hồi tại lần kiểm tra đó; điều này không chứng minh việc mất tin nhắn. Thử nghiệm nhỏ hơn vào ngày 29 tháng 10 dưới đây có chữ ký rõ ràng và xác minh chuỗi băm riêng.

## Các kiểm tra ngoại tuyến và kiểm tra tiêm lỗi gần đây · 1 tháng 11 năm 2026

Các kiểm tra này sử dụng dữ liệu giả định và tệp cục bộ; chúng cung cấp bằng chứng hồi quy cho nguồn hiện tại, chứ không phải một phép đo giao nhận Telegram thực tế khác:

| Kiểm tra | Những gì đã được kiểm tra |
| --- | --- |
| [Tập tin lưu trữ nguồn](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Hai bản dựng có các byte nguồn giống hệt nhau nhưng thời gian tạo tệp khác nhau đã tạo ra cùng một tệp ZIP và tổng kiểm tra. Các byte lưu trữ chính xác và các hàm băm tệp khớp nhau; các tệp thử nghiệm riêng tư vẫn được giữ nguyên. Một lỗi ghi mô phỏng đã để lại tệp lưu trữ và tổng kiểm tra trước đó nguyên vẹn. |
| [Khôi phục dữ liệu xuất tài khoản](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | Một lỗi đĩa mô phỏng trên thành viên ZIP thứ hai không để lại tệp ZIP nào được công bố hoặc tệp ZIP không đầy đủ. Chức năng tiếp tục tải xuống đã giữ nguyên từng byte của biên nhận đã ký, tạo ra một tệp lưu trữ có thể xác minh độc lập bằng cách sử dụng dấu vân tay ký tên dự kiến, và giữ lại khoảng trống phạm vi tổng hợp như một kết quả không đầy đủ. Các khẳng định về quy mô giúp ngăn chặn việc quét lặp lại các tác vụ và biên nhận khi lịch sử ngày càng dài. |
| [Bảo mật thông tin tối thiểu](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Các tên và biệt danh Unicode tổng hợp, siêu dữ liệu lồng nhau, người gửi chưa xác định và các trường phương tiện đã được kiểm tra trong cả ba chế độ nhận dạng và trong trường hợp thiếu văn bản. Lỗi giới hạn che giấu không làm suy yếu quá trình che giấu một cách âm thầm; tệp xuất tài khoản đã ký gốc vẫn giữ nguyên. |
| [Bộ giải mã phương tiện Linux và OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | Một [kiểm tra CI Docker trên Linux](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) tại commit `5a9e0814` đã vượt qua các đầu vào được tạo ra ở định dạng Ogg/Opus, MP3, M4A, MP4 kèm video, WAV và FLAC; các kiểm soát về thời lượng giả mạo và tham chiếu tệp thứ cấp; cùng 48 bộ dữ liệu thử nghiệm trình phân tích cú pháp đã biến đổi (34 bộ bị từ chối, 14 bộ được giải mã trong giới hạn). OCR Tesseract thực tế hoạt động mà không thay đổi các byte gốc. Trình giải mã và OCR chạy trong các container cách ly mạng mà không cần mô hình Whisper. |

Các kiểm tra được thực hiện trong các quy trình làm việc [(yêu cầu kéo)](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) và [(kiểm tra đầy đủ)](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml). Chúng kiểm tra các giới hạn lỗi này, chứ không phải mọi lỗi lưu trữ có thể xảy ra hoặc liệu việc tiết lộ thông tin có tự động an toàn để công bố hay không. Kiểm tra phương tiện truyền thông không đo lường độ chính xác của nhận dạng giọng nói hoặc khả năng gửi tin nhắn trên Telegram. Hãy xem xét kỹ từng bản sao trước khi chia sẻ.

## Thử nghiệm Telegram trực tiếp, toàn bộ tài khoản · Ngày 29 tháng 10 năm 2026

Tài khoản này vẫn tiếp tục hoạt động sau thử nghiệm dưới đây. Vào lúc 12:10 UTC ngày 29 tháng 10, phạm vi ghi chép đã được chuyển sang toàn bộ tài khoản (kênh, nhóm, cuộc trò chuyện riêng tư và bot); bảng điều khiển đã yêu cầu xác nhận và sổ nhật ký có chữ ký đã ghi lại thao tác này. Đến 17:59 UTC, sổ nhật ký ghi nhận:

| Thời gian ghi lại: từ 21:36 ngày 27 tháng 10 đến 17:59 ngày 29 tháng 10 theo giờ UTC | Số lượng |
| --- | --- |
| Các bản ghi trong sổ chứng cứ | 9,968 |
| Tin nhắn mới | 5,308 |
| của họ sau khi chuyển sang tài khoản đầy đủ | 3,878 |
| Các hành động xóa | 784 |
| trong số đó đã bị xóa sau khi TgWitness đã lưu lại tin nhắn | 596 |
| Các chỉnh sửa | 41 |
| Các tin nhắn được bổ sung sau khi kiểm tra lại | 2,273 |
| Các tin nhắn mà quá trình kiểm tra lại không thể tìm thấy được nữa | 18 |
| Các tin nhắn được lưu trữ thông qua các bản chụp lịch sử | 242 |
| Tệp đính kèm đã lưu | 247 |
| Trình thu thập bắt đầu | 19 |
| Telegram FloodWait tạm dừng | 26 |

- Chức năng kiểm tra **“Verify”** của ban chuyên gia đã xác nhận các chữ ký và chuỗi băm của toàn bộ 9.968 bản ghi.
- Các tin nhắn này đến từ 2 nhóm hoặc kênh và 3 cuộc trò chuyện riêng tư cùng các bot. Một nút gửi tin nhắn đã được nhấn từ **mục Trò chuyện**; yêu cầu và phản hồi của Telegram đều được ghi lại trong sổ nhật ký.
- Các cuộc trò chuyện mới đã được thêm vào khi trình thu thập dữ liệu quét lại tài khoản sau khi khởi động lại. Tính năng lưu trữ các tin nhắn trước đó của các cuộc trò chuyện mới đã bị tắt (`history = 0`), do đó nội dung này không được đề cập tại đây.

Không bao gồm: các phản ứng, thay đổi thành viên, hồ sơ cá nhân, việc gửi tin nhắn, tham gia qua lời mời, máy chủ proxy, thông báo, bot Witness và việc sử dụng nhiều tài khoản cùng lúc. Các tệp công khai chỉ chứa số liệu thống kê.

## Tệp xuất được bảo vệ bằng mật khẩu, mở bằng libarchive · Ngày 29 tháng 10 năm 2026

Một tệp lưu trữ được tạo bởi mã mã hóa xuất (WinZip AES-256, định dạng mà 7-Zip và WinRAR có thể đọc) đã được mở bằng Windows `tar` (bsdtar 3.6.2, libarchive). Khi nhập mật khẩu chính xác, tệp đã giải nén trùng khớp với giá trị SHA-256 ban đầu; mật khẩu sai sẽ bị từ chối với thông báo “Mật khẩu không chính xác”. Bản thân các phần mềm 7-Zip và WinRAR không được khởi chạy.

## Thử nghiệm Telegram trực tiếp · Từ ngày 27 đến ngày 29 tháng 10 năm 2026

Một tài khoản Telegram thực, được đăng nhập thông qua nhóm cặp API tích hợp sẵn, đã ghi lại một siêu nhóm từ **21:36 UTC ngày 27 tháng 10 đến 05:15 UTC ngày 29 tháng 10**. Trình thu thập dữ liệu đã được khởi động 12 lần trong khoảng thời gian đó.

| Đã ghi lại | Số lượng |
| --- | --- |
| Các bản ghi nhật ký, bao gồm các bản ghi hoạt động định kỳ và bản ghi dịch vụ | 2,385 |
| Tin nhắn mới | 1,291 |
| Các hành động xóa | 472 |
| trong số đó đã bị xóa sau khi TgWitness đã lưu lại nội dung văn bản | 347 |
| Các chỉnh sửa | 12 |
| Các tin nhắn bị bỏ sót trong thời gian ngừng hoạt động đã được bổ sung thông qua quá trình kiểm tra lại | 12 |
| Tệp đính kèm đã lưu | 17 |
| Các tệp đính kèm chưa được tải xuống (chức năng tải xuống bị tắt hoặc không có tệp để tải xuống) | 14 |
| Telegram FloodWait sẽ tạm dừng, mỗi lần 3 giây, trong quá trình kiểm tra lại | 8 |

- Các chữ ký và chuỗi băm của toàn bộ 2.385 bản ghi đều được xác minh dựa trên khóa công khai của sổ nhật ký.
- Sau khi khởi động lại, trình thu thập dữ liệu sẽ tiếp tục từ trạng thái cập nhật đã lưu (`pts`) và Telethon sẽ tiến hành đồng bộ hóa; quá trình kiểm tra lại sau đó sẽ bổ sung các tin nhắn còn thiếu.
- Trong mỗi lần FloodWait, bộ thu thập sẽ chờ trong khoảng thời gian được yêu cầu rồi tiếp tục hoạt động.
- Tài khoản vẫn duy trì trạng thái đăng nhập, và cùng phiên làm việc đó đã kết nối lại vào ngày 29 tháng 10.

Những nội dung sau đây không nằm trong phạm vi kiểm tra này: việc quản lý nhiều tài khoản cùng lúc, vai trò quản trị viên, máy chủ proxy, các sự cố ngừng hoạt động kéo dài hơn vài giờ và toàn bộ [quy trình chấp nhận trực tiếp](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Các tệp công khai chỉ chứa các số liệu thống kê này: không bao gồm thông tin nhận dạng tài khoản hay cuộc trò chuyện, tin nhắn hoặc thông tin đăng nhập.

## Đo lường năng lực địa phương tổng hợp

Lệnh: `python tools/check_capacity.py --events 10000 --chats 100`

| Chỉ số | Đã quan sát |
| --- | --- |
| Nội dung đầu vào | 10.000 sự kiện tin nhắn tổng hợp từ 100 nguồn tổng hợp được lựa chọn |
| Nội dung tin nhắn | 400 ký tự; không kèm phương tiện truyền thông hoặc thông tin mạng |
| Quá trình nhập dữ liệu | 53,273 giây; 187,7 sự kiện/giây |
| Độ trễ của trình xử lý | p50 4,162 ms; p95 7,784 ms; tối đa 129,118 ms |
| Xuất dưới dạng ZIP | 19,868 giây khi bật tracemalloc |
| Phân bổ xuất Python được theo dõi ở mức cao nhất | 0,51 MiB; không hỗ trợ RSS |
| Kích thước tệp ZIP | 4.610.962 byte |
| Xác minh độc lập | Tất cả 10.000 sự kiện đã được xác minh |

Chỉ số này đo lường đường dẫn ghi lại/xuất dữ liệu cục bộ trên máy chủ Windows này. Chỉ số này không đo lường việc truyền tải qua MTProto, số lượng tài khoản đồng thời, việc giới hạn băng thông của Telegram, tệp đa phương tiện, tải công việc kéo dài, hay số lượng cuộc trò chuyện thực tế được đảm bảo. Việc đo lường này được thực hiện trước khi công cụ đóng dấu thời gian ngoại tuyến cuối cùng được triển khai, và công cụ này không làm thay đổi đường dẫn tin nhắn đã được đo lường.

## Tìm kiếm toàn văn trên một triệu tin nhắn · 5 tháng 11 năm 2026

Lệnh: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Một nhật ký có chữ ký xác định gồm 1.000.000 tin nhắn tổng hợp trong 200 cuộc trò chuyện (các dạng từ tiếng Nga, tiếng Ukraina, tiếng Anh, tiếng Trung, tiếng Nhật, các liên kết và tên người dùng) đã được lập chỉ mục trong 71 giây; chỉ mục chiếm 58 MiB bên cạnh nhật ký 1,50 GiB. Các tìm kiếm phù hợp nhất mất từ 9 đến 190 ms (giá trị trung vị), so với 2,4 đến 3,2 giây cho tìm kiếm chuỗi con trước đó. Kết quả đầy đủ, phần cứng và giới hạn: [Tìm kiếm toàn văn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#benchmark). `tools/test_fulltext.py` cũng xác minh một tệp lưu trữ đã ký được tạo trước khi tìm kiếm toàn văn (`tools/fixtures/evidence-before-fulltext.zip`) bằng trình xác minh hiện tại, và một tập tin lưu trữ hiện tại với chính tập tin lưu trữ đó `verify.py`.

## Các tiêu chí còn lại

Nhật ký trực tiếp được lưu giữ này ghi nhận chính xác các hoạt động thu thập, chỉnh sửa, thông báo xóa, tệp đính kèm, việc kiểm tra lại và xử lý giới hạn tốc độ. Nó không ghi lại toàn bộ quá trình gửi tin nhắn hay một ma trận được kiểm soát về phạm vi hiển thị theo vai trò, các chủ thể phản ứng, thời gian chờ FloodWait kéo dài, việc khóa tài khoản và quá trình khôi phục sau sự cố gián đoạn mạng/quy trình. Việc phát hành mã QR-token vẫn tách biệt với quá trình xác nhận mã QR trên thiết bị di động đã hoàn tất.

Các kiểm tra Docker/Compose và cài đặt được ghi lại trong CI; việc triển khai Phala thực tế và xác minh dấu thời gian bên ngoài được mô tả ở trên. Chúng không thiết lập tải trọng cao liên tục, ma trận nền tảng/vai trò trực tiếp hoàn chỉnh, đánh giá bảo mật độc lập , xác thực lưu trữ dài hạn hoặc chứng nhận pháp y. Trạng thái MTProto đã lưu và cơ chế bù đắp đã được triển khai; việc phát lại trực tiếp nguyên tử không mất dữ liệu vẫn chưa được thiết lập. Phiên bản mới hơn thực hiện việc điền lại các thông điệp và con trỏ một cách nguyên tử và bảo toàn các Hành động Gần đây có sẵn, nhưng phạm vi bao phủ tổng hợp của nó khác biệt so với quá trình kiểm định trực tiếp. Xem [(chấp nhận trực tiếp) và](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) để biết ma trận kiểm định có kiểm soát.

Thư mục kiểm toán công khai  chỉ chứa báo cáo đã ký và các số liệu tổng hợp. Các biên lai hoạt động chi tiết, dữ liệu ghi lại thô và tài liệu tài khoản vẫn được giữ riêng tư. Các ảnh chụp màn hình ứng dụng trong `docs/assets/` sử dụng dữ liệu minh họa hư cấu.
