# Tìm kiếm toàn văn

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/

Tìm các tin nhắn đã lưu theo dạng từ, cụm từ chính xác, tên miền và @tên người dùng, hiển thị kết quả phù hợp nhất trước tiên, với chỉ mục được liên kết với nhật ký có chữ ký.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/vi/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Phân tích kho lưu trữ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/analysis/) · [OCR và chuyển đổi văn bản tại địa phương](https://phishdestroy.github.io/TgWitness/vi/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Xem trước.** Trong **Nhật ký**, chọn **"Kết quả phù hợp nhất · các dạng từ**" bên cạnh trường tìm kiếm. Kết quả được xếp hạng theo thuật toán BM25 và bao gồm các dạng khác của cùng một từ: *"перевод"* sẽ tìm thấy *"переводом"* và *"переводы"*, *"transfer"* sẽ tìm thấy *"transfers"*, một cụm từ tiếng Trung sẽ được tìm thấy mà không cần khoảng trắng. Chế độ "**Mới nhất trước · văn bản chính xác"** duy trì tìm kiếm chuỗi con trước đó trên toàn bộ bản ghi.

Chỉ mục là dữ liệu được trích xuất. Nó được tái tạo từ nhật ký đã ký, bản thân nó không bao giờ được ký và không bao giờ được xuất ra. Các bản ghi gốc không bị thay đổi.

**On this page**

- [Search syntax](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#search-syntax)
- [Languages](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#languages)
- [Where the index lives](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#where-the-index-lives)
- [Results and the signed journal](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#results-and-the-signed-journal)
- [Recognized text](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#recognized-text)
- [Access](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#access)
- [Ask the archive and MCP](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#ask-the-archive-and-mcp)
- [Dependencies](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#dependencies)
- [Benchmark](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/#benchmark)

## Cú pháp tìm kiếm

| Viết | Tìm kiếm |
| --- | --- |
| `перевод карта` | Các bản ghi chứa cả hai từ, dưới bất kỳ hình thức nào |
| `"переводом на карту"` | Cụm từ chính xác, theo thứ tự này |
| `бонус OR подарок` | Bất kỳ từ nào |
| `перевод -казино` | Các bản ghi không chứa từ bị loại trừ |
| `example.com` | Tên miền và các tên miền con của nó, bao gồm cả trong các liên kết ẩn và URL của các nút |
| `@username`, `t.me/username` | Các đề cập và liên kết đến tài khoản, cùng các tin nhắn mà tài khoản đó đã gửi |
| `#tag` | Thẻ hashtag |
| `+79991234567`, một địa chỉ ví, một địa chỉ email | Giá trị tương tự dưới dạng văn bản hoặc liên kết |
| `from:@username`, `from:123456` | Các tin nhắn từ người gửi đó |
| `chat:-1001234567890` | Một cuộc trò chuyện; nó chỉ có thể hạn chế quyền truy cập của chính bạn |
| `id:42` | Các phiên bản đã lưu của tin nhắn số 42 |
| `since:2026-01-01 until:2026-01-31` | Thời gian quan sát; một ngày không kèm giờ sẽ bao gồm cả ngày |
| `kind:edited` | Chỉ chỉnh sửa (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Văn bản được nhận diện thay vì, hoặc cùng với, các tin nhắn |

Các giới từ và từ chức năng khác sẽ bị bỏ qua khi có các từ khác xuất hiện. Các chữ cái trông giống nhau xen kẽ trong một từ (chữ *a* La-tinh nằm trong một từ Cyrillic), các ký tự Unicode có chiều rộng đầy đủ và trang trí, cũng như các ký tự vô hình sẽ được chuẩn hóa.

## Ngôn ngữ

Ngôn ngữ được xác định cho từng bản ghi dựa trên kịch bản và các ký tự của nó:

| Tập lệnh | Phù hợp |
| --- | --- |
| Chữ Cyrillic | Các từ gốc tiếng Nga và tiếng Ukraina với [pymorphy3](https://github.com/no-plagiarism/pymorphy3). Nếu không có từ điển tiếng Ukraina tùy chọn, công cụ sẽ sử dụng một bộ phân tích gốc tiếng Ukraina nhẹ. |
| Tiếng Latinh | Bộ phân tích từ gốc Snowball tiếng Anh; các dấu phụ được bỏ qua |
| Tiếng Trung, Tiếng Nhật, Tiếng Hàn, Tiếng Thái, Tiếng Lào, Tiếng Khmer, Tiếng Miến Điện | Các cặp ký tự trùng lặp: bất kỳ cụm từ nào cũng được tìm thấy mà không có khoảng trắng. Các truy vấn tiếng Trung được tách thành các từ bằng jieba |
| Các tập lệnh khác | Các từ chính xác |

Từ điển tiếng Ukraina (`pymorphy3-dicts-uk`) được phân phối theo giấy phép GPL-3.0, do đó nó không được cài đặt theo mặc định. Hãy cài đặt nó bằng lệnh `pip install "tgwitness[uk-dictionary]"`; chỉ mục sẽ nhận diện trình phân tích mới và tự động xây dựng lại.

## Vị trí lưu trữ chỉ mục

| Chế độ | Lưu trữ | Cách sử dụng |
| --- | --- | --- |
| Trên đĩa (mặc định) | `search/fulltext.sqlite3` trong thư mục workspace | Các kho lưu trữ lớn; vẫn hoạt động bình thường sau khi khởi động lại |
| Chỉ lưu trong bộ nhớ | Không lưu trữ dữ liệu trên đĩa; được xây dựng lại mỗi khi khởi động | Không lưu bản sao nội dung tin nhắn trên đĩa |
| Tắt | Không có chỉ mục; Hiển thị **từ mới nhất trước ·** giữ nguyên **văn bản chính xác** | Cài đặt tối thiểu |

Quản trị viên chính chọn chế độ trong **mục Nhật ký → Bộ lọc → Chỉ mục tìm kiếm** cho từng không gian làm việc. `TGWITNESS_FULLTEXT=disk|memory|off` thiết lập giá trị mặc định cho các không gian làm việc chưa có lựa chọn riêng. Chuyển sang chế độ lưu trữ trong bộ nhớ hoặc tắt sẽ xóa tệp. Tệp chỉ mục có mức độ bảo vệ tương tự như nhật ký: nó được lưu trữ trong thư mục dữ liệu riêng tư . Tệp này không được mã hóa và không nằm trong các bản sao lưu hoặc bản sao lưu ngoài hệ thống.

Các bản ghi mới được lập chỉ mục ở chế độ nền trong vòng vài giây; khi tìm kiếm, hệ thống cũng ưu tiên lập chỉ mục các bản ghi tồn đọng gần đây nhất, do đó bản ghi vừa được lưu cách đây một lúc sẽ được tìm thấy. Một nhật ký hiện có sẽ được lập chỉ mục sau khi cập nhật mà không làm gián đoạn hoạt động của bảng điều khiển; cho đến lúc đó, kết quả tìm kiếm sẽ bao gồm các bản ghi đã được lập chỉ mục và nhật ký sẽ hiển thị tiến trình. **Quá trình xây dựng lại chỉ mục** sẽ bắt đầu lại từ bản ghi đầu tiên.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` cần dừng bảng điều khiển (mã thoát là 3 nếu không). Với `--json`, đầu ra tiêu chuẩn chỉ hiển thị kết quả; tiến trình được ghi vào đầu ra lỗi tiêu chuẩn.

## Kết quả và nhật ký được ký điện tử

Chỉ mục lưu trữ số thứ tự và giá trị băm của bản ghi nhật ký cuối cùng mà nó bao phủ và đối chiếu chúng với nhật ký khi mở. Một nhật ký bị thay thế, khôi phục hoặc chỉnh sửa sẽ gây ra quá trình xây dựng lại. Mỗi phản hồi báo cáo vị trí này, và mỗi kết quả khớp được đọc lại từ nhật ký có chữ ký thông qua số thứ tự của nó: chỉ mục quyết định những bản ghi nào sẽ hiển thị và theo thứ tự nào, chứ không bao giờ là nội dung của chúng. Quyền truy cập trò chuyện được áp dụng cho trường trò chuyện riêng của nhật ký, chứ không phải nội dung của chỉ mục.

## Văn bản được nhận diện

Dữ liệu OCR và bản chép lời vẫn được lưu trữ trong các tệp mã hóa của chúng. Chỉ mục của chúng chỉ tồn tại trong bộ nhớ và được xây dựng lại khi một tác vụ nhận dạng hoàn tất. Một kết quả khớp sẽ xuất hiện trong `media.saved` bản ghi đó, được gắn nhãn là “nhận diện tự động” kèm theo công cụ, mô hình và một đoạn trích; nó không bao giờ được hiển thị dưới dạng văn bản đã gửi trên Telegram. Chỉ mục này cũng được sử dụng cho **tính năng Tìm kiếm văn bản đã nhận diện**, vốn vẫn hỗ trợ so khớp với các chuỗi con thuần túy.

## Truy cập

Quyền truy cập trong phạm vi cuộc trò chuyện chỉ tìm thấy các bản ghi từ các cuộc trò chuyện đó, bao gồm cả văn bản được nhận diện từ các tệp đính kèm của chúng. `chat:` và các bộ lọc khác chỉ có thể thu hẹp tập dữ liệu đó. Trạng thái chỉ mục hiển thị cho quyền truy cập theo phạm vi không bao gồm tổng số bản ghi trong nhật ký. Chỉ quản trị viên chính mới có thể thay đổi chế độ hoặc xây dựng lại chỉ mục.

## Hỏi kho lưu trữ và MCP

Khi quá trình lập chỉ mục hoàn tất,**hệ thống lưu trữ** sẽ truy xuất các nguồn từ chỉ mục này: các kết quả khớp tốt nhất trong các cuộc trò chuyện đã chọn, với mỗi đoạn văn bản được lưu chỉ được tính một lần. Tối đa 24 nguồn được gửi; các văn bản dài sẽ được cắt xung quanh phần khớp và được đánh dấu là bị cắt ngắn. Các câu hỏi về những thay đổi gần đây, các phiên bản đã lưu của một tin nhắn và các tìm kiếm trong khi chỉ mục vẫn đang được xây dựng sẽ sử dụng phương thức truy xuất theo thứ tự thời gian trước đó. Bản xem trước hiển thị phương thức nào đã được sử dụng.

Các khách hàng MCP có thể gọi `search_messages` với `ranked=true` và truy cập trang với `next_offset`. Các kết nối có phạm vi chỉ nhận được các cuộc trò chuyện của riêng họ.

Ranked pagination covers at most the first 1,000 results, regardless of page size. Narrow the query, chat or period to inspect further matches. Newest-first searches order messages, OCR and transcription results before selecting each page.

## Các thành phần phụ thuộc

| Gói | Giấy phép | Tại sao |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Các từ gốc tiếng Nga và tiếng Ukraina; các từ điển được tải cục bộ |
| snowballstemmer | BSD-3-Clause | Các từ gốc tiếng Anh, Python thuần túy |
| jieba | MIT | Phân đoạn truy vấn tiếng Trung, viết hoàn toàn bằng Python (chỉ phân phối mã nguồn) |
| pymorphy3-dicts-uk (tùy chọn) | GPL-3.0 | Từ điển tiếng Ukraina đầy đủ |

SQLite FTS5 yêu cầu có `unicode61` tokenizer; nó là một phần của SQLite trong các bản dựng Python hiện tại. Nếu thiếu nó, tính năng tìm kiếm kết quả phù hợp nhất sẽ báo lỗi rằng tính năng này không khả dụng.

## Đánh giá hiệu năng

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`tạo ra một nhật ký có chữ ký xác định trước chứa các tin nhắn hỗn hợp bằng tiếng Nga, tiếng Ukraina, tiếng Anh, tiếng Trung và tiếng Nhật kèm theo các liên kết và mã định danh trong 200 cuộc trò chuyện, xây dựng chỉ mục và đo thời gian thực hiện các tìm kiếm điển hình (50 kết quả, giá trị trung vị của 7 lần chạy).

Được đo trên Windows 11, Intel Core i9-13900K, 128 GB RAM, Python 3.12.10, SQLite 3.49.1, dữ liệu trên ổ đĩa exFAT, trình phân tích `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Đo lường | Kết quả |
| --- | --- |
| Nhật ký được ký điện tử | 1.000.000 tin nhắn, 1,50 GiB, được ghi lại trong 19 phút |
| Xây dựng chỉ mục từ nhật ký | 71 giây, khoảng 14.141 tin nhắn mỗi giây |
| Tệp chỉ mục | 58 MiB, chiếm 3,8% dung lượng nhật ký |
| Tìm kiếm ngay sau một bản ghi mới | Giá trị trung vị là 8 ms, p95 là 9 ms |
| Tìm kiếm chuỗi con trước đó, cùng một nhật ký | `перевод` 3,2 giây, `银行转账` 2,6 giây, `verify-account.example` 2,6 giây |

| Tìm kiếm | Các bản ghi khớp nhau | Kết quả phù hợp nhất, giá trị trung vị | trang 95 | Mới nhất trước, trung bình |
| --- | --- | --- | --- | --- |
| Từ thông dụng, các dạng từ: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Hai từ: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Từ hiếm: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Cụm từ chính xác: `"переказ коштів на картку"` | không được tính | 35 ms | 36 ms | 6 ms |
| Tên miền cùng các tên miền con: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @username: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Tiếng Trung không có khoảng trắng: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Tiếng Nhật: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Cơ sở tiếng Anh: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| HOẶC và loại trừ: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Bộ lọc cuộc trò chuyện: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Bộ lọc theo khoảng thời gian: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Một cụm từ chính xác sẽ được kiểm tra theo nghĩa đen trên các kết quả theo thứ tự xếp hạng cho đến khi trang đầy, do đó tổng số kết quả của nó không được tính. Thời gian xử lý tăng theo số lượng bản ghi khớp; hạn chế phạm vi cuộc trò chuyện hoặc khoảng thời gian sẽ giúp các tìm kiếm rộng diễn ra nhanh hơn. Bộ dữ liệu tổng hợp lặp lại một số từ vựng hạn chế, do đó các từ thông dụng sẽ khớp với nhiều bản ghi hơn so với trong các cuộc trò chuyện thực tế.
