# Những nội dung đã được kiểm thử

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/

Thử nghiệm Telegram trực tiếp, các kiểm tra tự động, kiểm tra trên trình duyệt và những nội dung vẫn chưa được xác minh.

## Triển khai trên Phala Cloud · Ngày 4 tháng 11 năm 2026

`--provider phala --quick-tunnel` đã được chạy trên môi trường thực tế **Phala Cloud** (`tdx.small`, khu vực US-WEST-1) với khóa API Phala Cloud của một không gian làm việc trống, tệp ntfy.sh thực tế, GitHub và Intel PCS. CVM đã cài đặt bản cam kết `df7d860c` (phiên bản 0.8.1); các thao tác triển khai, xác minh và hủy bỏ được thực hiện từ dòng lệnh với các bản sửa lỗi dưới đây. Tổng chi phí cho bảy CVM là khoảng 1,9 xu Mỹ.

Hai lần triển khai đầu tiên đã phát hiện ra năm điểm khác biệt so với Phala Cloud mô phỏng. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) hiện đã tái hiện từng trường hợp này và sẽ thất bại nếu không có bản sửa lỗi tương ứng:

| Trên Phala Cloud | Trước khi khắc phục | Sửa lỗi |
| --- | --- | --- |
| Yêu cầu phải có `compose_file.name` | Lỗi HTTP 422, không tạo được gì | Cấu hình Docker Compose chứa tên CVM |
| Trừ khi được cung cấp một giá trị trống, Phala sẽ tự động thêm tập lệnh khởi động trước của riêng mình vào tệp app-compose được đo lường (phiên bản v0.0.20: thông tin đăng nhập Docker, `docker compose pull`, mật khẩu root, khóa SSH từ `user_config`) | `tdx_compose` không thành công: mã nằm ngoài cấu hình Docker Compose đã được công bố | Tệp app-compose đặt `pre_launch_script` thành `""`; Phala sau đó sẽ bỏ qua phần này |
| Nếu không có `image`, Phala sẽ chọn `dstack-dev-0.5.12`, phiên bản phát triển, với quyền truy cập SSH được kích hoạt | `server_state` không thành công. Chỉ riêng bản ghi chứng thực phần cứng là đã đạt yêu cầu trên hình ảnh này; chỉ có bản ghi nhà cung cấp và `tdx_os` mới thể hiện điều này | Quá trình triển khai yêu cầu bản dựng sản xuất của phiên bản Phala hiện tại, `dstack-0.5.12` |
| Khi cổng dstack bị tắt, thông tin chi tiết về CVM không bao giờ hiển thị mã lỗi `instance_id` | Quá trình triển khai chờ 30 phút rồi thất bại | ID phiên bản được đọc từ trạng thái CVM |
| Các thao tác khởi động lại, dừng và khởi động là các thao tác trên CVM, không phải các bản cập nhật ứng dụng | `provider_actions` không liệt kê các lần khởi động lại | Các thao tác này cũng được ghi nhận |

Lần triển khai thứ ba:

- CVM đã chạy `dstack-0.5.12` với quyền truy cập SSH bị tắt. Bộ thu thập đã đăng địa chỉ đã ký của mình khoảng 1,5 phút sau khi được tạo. Quá trình triển khai sau đó đã thông qua `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, bản ghi chứng thực phần cứng v4, FMSPC `20a06f000000`, không ở chế độ gỡ lỗi, không thể di chuyển, hỗ trợ dữ liệu xác minh mật mã lấy từ Intel), `tdx_compose_hash`, `tdx_compose` (từng byte) và `tdx_identity` (khóa KMS).
- Bảng điều khiển tại địa chỉ trycloudflare.com trả về mã trạng thái 401 khi không có mã thông báo hoặc sử dụng mã thông báo sai, và trả về mã trạng thái 200 khi sử dụng mã thông báo của bảng điều khiển.
- `verify` với `--source` được thiết lập trỏ đến kho lưu trữ cam kết trên GitHub và dấu vân tay được truyền riêng biệt: máy chủ, `server_state`, tường lửa (không có cổng, không có điểm cuối công khai), nhật ký nhà cung cấp, báo cáo, dấu vân tay, băm nguồn, quá trình khởi động và năm kiểm tra `tdx_*` đều đạt yêu cầu. Cloudflare và `tdx_os` không khả dụng, do đó kết quả là CHƯA HOÀN THÀNH.
- Hai lần khởi động lại thông qua API của Phala: mỗi lần, CVM đều hoạt động trở lại trong vòng chưa đầy hai phút với cùng một khóa thu thập, một địa chỉ đã ký mới và địa chỉ cũ trả về mã trạng thái 530. `verify` đã báo cáo lần khởi động mới và cả hai lần khởi động lại với trạng thái REVIEW. Với `--evidence`, hệ thống đã xác nhận các chữ ký nhật ký và ba lần khởi động, mỗi lần đều có bản ghi chứng thực phần cứng Intel TDX riêng từ cùng một CVM.
- Lệnh `destroy` chỉ xóa CVM đó. Sau đó, không gian làm việc trở nên trống rỗng và địa chỉ bảng điều khiển ngừng phản hồi.
- Kết quả kiểm tra giá trên trình hướng dẫn bảng điều khiển hiển thị `tdx.small` với mức giá 0,058 USD mỗi giờ. Khi nhập sai khóa, hệ thống sẽ hiển thị thông báo đơn giản “không chấp nhận khóa API”.

Hai phát hiện khác, đã được khắc phục sau đó:

- Nếu không có khóa địa chỉ, `verify` sẽ tuân theo bài đăng hợp lệ mới nhất về chủ đề địa chỉ, được in trong cấu hình Docker Compose đã công bố. Một bài đăng giả mạo đã gửi nó đến một máy chủ không tồn tại, và `statement` đã thất bại: kẻ giả mạo không thể giả danh là người thu thập, nhưng có thể ngăn chặn quá trình xác minh của bên thứ ba, trong tối đa 12 giờ bằng cách sử dụng dấu thời gian giả mạo trong tương lai. Hiện tại, bộ thu thập cũng đăng địa chỉ của mình kèm chữ ký bằng khóa riêng, `verify` chỉ chấp nhận các bài đăng như vậy khi chính bộ thu thập tạo ra chúng, và các bài đăng được sắp xếp theo thời gian nhận của ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) phát lại các bài đăng giả mạo. Một CVM chỉ chạy quy trình này từ một bản cam kết (commit) chứa nó, do đó người thu thập của lần chạy này chưa ký địa chỉ của mình và `verify` đã thông báo điều đó.
- `tdx_os` không thể chạy nếu thiếu `dstack-mr`; phiên bản hiện tại của công cụ này có lệnh `measure-os` thay vì `measure --json` được nêu trong tài liệu. Công cụ xác minh hiện tự tính MRTD và RTMR0-2 từ ảnh hệ điều hành đã công bố và cấu hình máy ảo, bao gồm các bảng ACPI.

Lần triển khai thứ tư, bao gồm các thành phần sau:

- Quá trình triển khai đã tải xuống tệp `dstack-0.5.12` đã được công bố một lần, đối chiếu nó với băm hình ảnh hệ điều hành mà CVM báo cáo, và tệp `tdx_os` đã vượt qua kiểm tra: các giá trị MRTD, RTMR0, RTMR1 và RTMR2 trùng khớp với các giá trị được tính toán cho QEMU 8.2.2, 1 vCPU và 2 GiB. Cùng một phép tính này lại cho kết quả RTMR0 khác khi đối với cấu hình được khai báo là 4 GiB, 2 vCPU, QEMU 9.2.1 hoặc có thêm thẻ mạng thứ hai, và không đạt yêu cầu khi nhân hệ điều hành, phần sụn hoặc dòng lệnh bị thay đổi cũng như đối với hình ảnh phát triển.
- `verify` đã vượt qua toàn bộ 16 bài kiểm tra, bao gồm cả bộ kết nối của đường hầm nhanh, do đó kết quả là ĐẠT. Hệ thống đã tạo ra chứng chỉ dưới dạng HTML và PDF, được niêm phong kỹ thuật số bằng chữ ký và dấu thời gian, bao gồm dấu thời gian eIDAS đủ điều kiện từ đơn vị đóng dấu thời gian TSU 202301 của Chính phủ Bỉ (tình trạng được cấp trên danh sách tin cậy của Bỉ), dấu thời gian FreeTSA và chữ ký của bên xác minh; `check-report` đã xác nhận tất cả các yếu tố này cùng với chữ ký trên tệp PDF.
- Sau khi khởi động lại, `verify --evidence` đã xác nhận hai lần khởi động, mỗi lần đều đi kèm với một chứng nhận phần cứng được tạo ra bên trong CVM và mỗi lần đều được khởi động từ `dstack-0.5.12` đã được công bố; cả lần khởi động lại và lần khởi động mới đều ở trạng thái REVIEW.
- `destroy` đã để không gian làm việc trống rỗng.

Lần triển khai thứ năm đã chạy trình thu thập dữ liệu từ bản cam kết `53a0f7e9`, bao gồm tất cả các yếu tố nêu trên:

- Bộ thu thập đã đăng địa chỉ của mình được ký bằng khóa riêng, ngay bên cạnh bài đăng HMAC của nhà điều hành. Sau đó, hai bài đăng giả mạo đã được thêm vào chủ đề này, một bài có HMAC bằng 0 và một bài được ký bằng một khóa Ed25519 khác, cả hai đều tuyên bố thời gian là năm 2096. `verify` đã lấy địa chỉ được ký bằng khóa của bộ thu thập và vượt qua tất cả 16 bước kiểm tra; con dấu này một lần nữa mang dấu thời gian đủ điều kiện của Bỉ, dấu thời gian của FreeTSA và chữ ký của bên xác minh, và `check-report` đã xác nhận các thông tin này.
- Sau khi khởi động lại, bộ thu thập đã đăng địa chỉ mới đã được ký: `verify` đã phát hiện ngay lập tức, **của nhà điều hành đã tìm thấy địa chỉ hiện tại** 27 giây sau đó từ bài đăng HMAC, và cả hai đều bỏ qua các bài đăng giả mạo. `verify --evidence` đã xác nhận hai lần khởi động từ `dstack-0.5.12`.
- Quá trình triển khai đã hiển thị mức phí mà Phala tính cho CVM, bao gồm cả đĩa: 0,06078 USD mỗi giờ.

Trình hướng dẫn bảng điều khiển đã chạy trên Phala Cloud hai lần, một lần thông qua API công việc của nền tảng này và một lần thông qua trình duyệt sử dụng Chromium thực: kiểm tra giá, tạo cấu hình với cam kết dưới **Advanced**, cả sáu kiểm tra chứng thực đều đạt yêu cầu, danh sách máy chủ hiển thị mức giá được tính (44,37 USD mỗi tháng), **Find địa chỉ hiện tại**, quá trình tải xuống cấu hình Docker Compose đã được đo lường, và quá trình xóa. Trình duyệt không ghi nhận bất kỳ lỗi trang nào. Sau mỗi lần thực hiện, không gian làm việc đều trống rỗng.

Không bao gồm: tên miền Cloudflare trên Phala, tài khoản Telegram trên CVM và hình ảnh `dstack-0.6.1`. Giá hiển thị trên trình hướng dẫn trước khi tạo chỉ bao gồm chi phí tính toán của Phala, do API của Phala chỉ liệt kê chi phí đĩa cho các CVM hiện có; danh sách máy chủ hiển thị giá được tính hóa đơn sau khi tạo.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Số lượng |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Kiểm tra | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

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

## Các tiêu chí còn lại

Nhật ký trực tiếp được lưu giữ này ghi nhận chính xác các hoạt động thu thập, chỉnh sửa, thông báo xóa, tệp đính kèm, việc kiểm tra lại và xử lý giới hạn tốc độ. Nó không ghi lại toàn bộ quá trình gửi tin nhắn hay một ma trận được kiểm soát về phạm vi hiển thị theo vai trò, các chủ thể phản ứng, thời gian chờ FloodWait kéo dài, việc khóa tài khoản và quá trình khôi phục sau sự cố gián đoạn mạng/quy trình. Việc phát hành mã QR-token vẫn tách biệt với quá trình xác nhận mã QR trên thiết bị di động đã hoàn tất.

Việc xây dựng/chạy Docker, cài đặt trên Linux/macOS, khả năng chịu tải cao liên tục, đánh giá bảo mật độc lập, phản hồi TSA độc lập thực sự, xác thực thu hồi/lưu trữ chứng chỉ và chứng nhận pháp y vẫn nằm ngoài phạm vi chứng nhận đã ghi nhận. Tình trạng MTProto đã lưu và tính năng bắt kịp đã được triển khai; tính năng phát lại nguyên tử bền vững vẫn chưa được thiết lập. Việc thu thập nhật ký quản trị, danh sách máy chủ phản hồi bổ sung và cơ chế thăm dò ưu tiên ngắn vẫn là các tính năng riêng biệt. Vui lòng tham khảo [bản chấp nhận trực tiếp](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) để xem ma trận chứng nhận có kiểm soát.

Các bản ghi chi tiết và ảnh chụp màn hình tại địa phương hiện được lưu trữ trong thư mục test-results/ (bị Git bỏ qua). Ảnh chụp màn hình công khai trong thư mục docs/assets/ chỉ chứa dữ liệu minh họa hư cấu.
