# Những nội dung đã được kiểm thử

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/

Thử nghiệm Telegram trực tiếp, các kiểm tra tự động, kiểm tra trên trình duyệt và những nội dung vẫn chưa được xác minh.

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
