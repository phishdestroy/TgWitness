# Cấu hình và xác minh báo cáo

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-reports/

Các bộ lọc báo cáo, tám mẫu thiết kế, cài đặt sẵn nội dung, lịch sử thay đổi đã lưu và phần đánh giá được bao gồm trong các tệp xuất có chữ ký.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Điều tra](https://phishdestroy.github.io/TgWitness/vi/docs/reference/investigation/)

![Điều tra](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

Chuyển các quan sát đã chọn thành một bản tường trình dễ đọc về vụ việc: câu hỏi, phạm vi, các thay đổi đã lưu, biểu đồ, kết quả và tham chiếu nguồn. Mỗi báo cáo cung cấp cho người nhận một cách để kiểm tra tài liệu được giao và xem xét phạm vi thu thập của nó.

Phần **“Cơ sở tin cậy và giới hạn**” xuất hiện trong các báo cáo nhật ký, bàn giao, trò chuyện, tài khoản và chia sẻ. Các tệp PDF nhật ký và bàn giao sử dụng cùng một bản đánh giá như tệp `report.json` đã được ký. Danh sách nội dung ZIP chứa thông tin đánh giá vụ việc (`case_assessment`) trong tệp danh sách nội dung đã được ký. Bản đánh giá này đi kèm với tài liệu được xuất ra. Các quan sát ban đầu vẫn giữ nguyên chữ ký hiện có của chúng.

## Định dạng tài liệu và thứ tự đọc

### Studio báo cáo

Mở **Exports → Cấu hình và xem trước**. Thực hiện theo trình tự **Data → Thiết kế & nội dung → Xem trước**:

1. Sử dụng toàn bộ không gian làm việc hoặc chọn các cuộc trò chuyện, tác giả, bao gồm cả ngày quan sát theo múi giờ UTC và các loại sự kiện. Tải danh mục để tìm kiếm các cuộc trò chuyện và tác giả, hoặc nhập ID Telegram của họ. Bộ lọc tác giả khớp với các ID người gửi đã được ghi lại; thông báo xóa không có người gửi sẽ không khớp với bộ lọc tác giả.
2. Chọn một thiết kế trang, sau đó chọn biểu đồ, nhãn người tham gia, bản ghi chép và kết luận bằng văn bản của bạn. Việc thay đổi thiết kế sẽ giữ nguyên các lựa chọn này.
3. Tạo bản xem trước. Bản xem trước hiển thị số liệu thực tế, hoạt động, người tham gia, các bản ghi mẫu, các thay đổi đã lưu và các khoảng số tin nhắn bị thiếu. Việc thay đổi lựa chọn sẽ khiến bản xem trước trở nên lỗi thời. Lưu lại trước khi tải xuống tệp HTML, PDF đã ký, JSON đã ký hoặc tệp ZIP chứa bằng chứng.

Bản xem trước dữ liệu tính toán tiền tố nhật ký ổn định hoàn chỉnh, không phải mẫu ban đầu. Chỉ các hàng mẫu được hiển thị và các danh sách dài mới bị giới hạn; số lượng bị bỏ qua của chúng được hiển thị. Việc xuất dữ liệu sau này sẽ tạo ra một bản chụp ổn định mới, do đó việc thu thập đang diễn ra có thể làm tăng các con số này. Phạm vi, số lượng và danh tính nguồn được bao gồm trong báo cáo đã ký. Việc mở hoặc xem trước biểu mẫu sẽ không lưu lại biểu mẫu đó.

**Hướng dẫn về thẩm quyền pháp lý.** Trong phần Chi tiết tài liệu, mở **Hướng dẫn về thẩm quyền pháp lý · tùy chọn** để chọn thẩm quyền pháp lý và thủ tục dân sự/thương mại hoặc hình sự. Phụ lục bao gồm cơ sở pháp lý, liên kết nguồn, ghi chú chuẩn bị và tình trạng nghiên cứu. Tóm tắt và giải thích bằng ngôn ngữ địa phương về các biện pháp bảo vệ dữ liệu thu thập là tùy chọn. Không có khu vực pháp lý nào được chọn theo mặc định. Các lựa chọn này thuộc về không gian làm việc và không được bao gồm trong các cấu hình bố cục đã lưu cũng như các thiết lập mặc định ngầm định về chia sẻ và sao chép. Xem [thiết lập mặc định, báo cáo được hỗ trợ và giới hạn nghiên cứu](https://github.com/phishdestroy/TgWitness/blob/main/docs/JURISDICTION_GUIDANCE.md) .

**Chọn bản sao dành cho người nhận.** Các biểu đồ và bản ghi chép sử dụng các bản ghi đã chọn. Tính toàn vẹn, việc lưu giữ và phạm vi bao quát mô tả toàn bộ nhật ký nguồn. Tệp ZIP chứa bằng chứng chứa các bản ghi gốc và tệp đính kèm. Sử dụng [quy trình bàn giao tối thiểu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#handover-extract) khi người nhận chỉ cần nhận dữ liệu đã chọn và được phép.

### Đọc các nội dung đã chỉnh sửa, đã xóa và các ID bị thiếu

Một chỉnh sửa sẽ hiển thị văn bản **"Trước"** và **"Sau"** đã lưu và làm nổi bật các từ đã thay đổi. Một thao tác xóa sẽ hiển thị phiên bản cuối cùng được lưu trước thông báo. Nếu không có nội dung trước đó được ghi lại, báo cáo sẽ nêu rõ điều này. Khi bạn chỉ chọn các chỉnh sửa hoặc thao tác xóa, các phiên bản trước đó vẫn có sẵn dưới dạng bối cảnh được gắn nhãn rõ ràng bên ngoài các bộ lọc. Các thông báo không liên quan sẽ không được thêm vào các lịch sử này.

**ID tin nhắn không được quan sát** là những khoảng trống giữa các số đã biết trong các cuộc trò chuyện đã chọn và khoảng ID được xác định theo ngày tháng. Mọi bản ghi nguồn đã biết đều được kiểm tra trước khi xác định một số là không được quan sát: việc lọc ra một tác giả khác, một loại sự kiện hoặc một ngày tháng không thể tạo ra khoảng trống giả. Các tin nhắn đã lưu liền kề được gắn nhãn là bối cảnh. Một số bị thiếu không chứng minh rằng tin nhắn đó đã tồn tại hoặc đã bị xóa; thông báo xóa và việc kiểm tra lại không thành công vẫn là các loại sự kiện riêng biệt.

### Chọn một thiết kế

Có sẵn tám mẫu thiết kế cho các báo cáo dưới dạng HTML (dạng nhật ký và cuộc trò chuyện đơn lẻ) và PDF có chữ ký. Các mẫu này sử dụng cùng một dữ liệu và phép tính, nhưng có bìa, kiểu chữ, tiêu đề chương, bảng và khoảng cách khác nhau.

| Thiết kế | Phong cách trình bày |
| --- | --- |
| Cổ điển | Một hồ sơ truyền thống với bìa màu tối và các phần được đánh số. |
| Biên tập | Trang tiêu đề có khung viền serif, lề rộng và thanh phân chia chương hẹp. |
| Tóm tắt | Bìa gọn gàng với lưng sách màu xanh hải quân, các tiêu đề ngắn gọn và bảng dữ liệu được sắp xếp sát nhau. |
| Phân tích | Bìa theo phong cách bảng khảo sát, các bảng biểu mô-đun và hình minh họa sử dụng phông chữ cố định. |
| Kỹ thuật | Một sổ đăng ký có kẻ ô, thanh tham chiếu được đánh số và các bảng so sánh chính xác. |
| Tổng quan | Bìa toàn cảnh, khoảng cách rộng rãi và các số liệu tóm tắt nổi bật. |
| Loạt bài đọc | Một thanh mục lục và các chương được nhóm lại cho các phần kết quả, phạm vi, thay đổi và nhật ký quan sát. |
| Sổ cái & ký quỹ | Các chương được đánh số với lề rộng, bảng biểu chính xác và bản ghi tin nhắn riêng biệt. |

Thiết kế được lưu theo từng không gian làm việc và ghi lại trong bản kê khai xuất có chữ ký. HTML hoạt động ngoại tuyến, hỗ trợ chế độ sáng và tối, và thích ứng với màn hình hẹp cũng như các ngôn ngữ viết từ phải sang trái. Các tệp PDF gốc sử dụng phông chữ đi kèm; thiết kế Editorial bao gồm phông chữ Noto Serif theo Giấy phép Phông chữ Mở SIL đi kèm. Chế độ đọc theo chuỗi và Ledger & margin cũng áp dụng cho tổng quan tài khoản, cuộc trò chuyện tài khoản và chia sẻ bản sao.

Các tệp PDF tiếng Trung, tiếng Nhật và tiếng Hàn cần có phông chữ phù hợp trên máy chủ, chẳng hạn như Noto Sans CJK, được cài đặt trên toàn hệ thống hoặc đặt trong thư mục `TGWITNESS_FONT_DIR`. Khi phông chữ này không có sẵn, tệp ZIP sẽ giữ lại các báo cáo HTML và JSON.

Hai thiết kế này bao gồm một nhật ký dễ đọc mà không cần JavaScript. Đối với các tệp xuất có dung lượng lớn, chế độ xem này chứa tối đa 500 bản ghi hoàn chỉnh trong giới hạn đầu vào 8 MiB; báo cáo ghi rõ giới hạn này và cung cấp liên kết đến trình xem đầy đủ cũng như các bản ghi nguồn. Thư mục tài khoản và chỉ mục mối quan hệ mô tả cùng một mẫu đọc đó, chứ không phải tất cả những người tham gia. Các biểu đồ nhật ký đầy đủ giữ phạm vi được nêu riêng biệt của chúng.

### Chọn nội dung

| Nội dung được định sẵn | Được bao gồm theo mặc định |
| --- | --- |
| Hồ sơ vụ việc | Hoạt động, thời gian quan sát, người tham gia, các cuộc trò chuyện và bản ghi chép cuộc trò chuyện. |
| Tóm tắt | Tổng quan về hoạt động mà không bao gồm thứ hạng của người tham gia hoặc bản ghi chép. |
| Xem xét hoạt động | Hoạt động, thời gian quan sát, người tham gia, các cuộc trò chuyện và nội dung, kèm theo nguồn tham chiếu và số liệu chính xác. |
| Báo cáo tùy chỉnh | Bạn có thể tự kết hợp các biểu đồ, bản ghi chép và bản xem trước theo ý muốn. |

Việc thay đổi cài đặt sẵn sẽ giữ nguyên thiết kế, chi tiết vụ việc và phân tích bằng văn bản của bạn. Các kiểm tra tính toàn vẹn, phạm vi bao phủ, giới hạn và hướng dẫn xác minh vẫn được duy trì trong mọi thiết kế. Các bản ghi nguồn trong tệp ZIP sẽ không bị thay đổi khi biểu đồ hoặc bản ghi chép bị ẩn.

Các **ghi chú kiểm tra** tùy chọn chứa câu hỏi, phương pháp, kết quả và kết luận do tác giả báo cáo viết. Trích dẫn tệp nguồn và số bản ghi trong phần kết quả. Chữ ký bảo toàn các tuyên bố do tác giả viết này cùng với báo cáo; các quan sát từ nguồn và cách diễn giải của tác giả vẫn có thể nhận diện được. Việc bàn giao được tối giản sẽ loại bỏ các ghi chú riêng tư này và các biểu đồ nhật ký đầy đủ. Các lựa chọn về biểu đồ và khám nghiệm áp dụng cho các báo cáo nhật ký.

Chọn hoạt động theo thời gian, bản đồ nhiệt theo ngày trong tuần/giờ theo múi giờ UTC, bảng xếp hạng người tham gia, bảng xếp hạng cuộc trò chuyện và thành phần bản ghi. Chọn 5–30 nhóm được xếp hạng và các biệt danh hoặc ID tài khoản trung lập của người tham gia. Người gửi không xác định và những người tham gia còn lại được hiển thị trong các hàng riêng biệt. Biệt danh chỉ ảnh hưởng đến biểu đồ; các bản ghi nguồn vẫn chứa danh tính thực của họ.

Bản xem trước thiết kế được cập nhật từ bản nháp chưa lưu bằng cách sử dụng các thành phần bìa, phần kiểm tra và biểu đồ sản xuất, giới hạn trong các kết quả khớp với 50.000 bản ghi nguồn đầu tiên. Bản xem trước dữ liệu bên dưới tính toán toàn bộ phần đã chọn. Bản xem trước này rõ ràng chưa được ký và không lưu lại các chỉnh sửa. Các nút Bìa và Biểu đồ chuyển đổi phần tương ứng. Đây không phải là bản xem trước PDF hoàn chỉnh. **Lưu cài đặt báo cáo** sẽ áp dụng các lựa chọn cho các lần xuất trong tương lai; các tệp đã ký hiện có là không thể thay đổi. PDF sử dụng trang bìa đã chọn, kiểu chữ, bố cục chương và các tổng hợp đã chọn giống như HTML và JSON đã ký.

Đánh giá độ tin cậy, giới hạn phạm vi và hướng dẫn xác minh vẫn được giữ nguyên. Việc ẩn các biểu đồ hoặc bản ghi chép có thể đọc được không loại bỏ các hàng nguồn có thẩm quyền khỏi tệp ZIP. Các chuỗi biểu đồ bị vô hiệu hóa sẽ bị loại bỏ khỏi tệp JSON phân tích; hãy sử dụng tính năng xuất tối thiểu để hạn chế việc tiết lộ các bản ghi nguồn.

Các bộ lọc chọn dữ liệu áp dụng cho báo cáo nhật ký; các tệp xuất tài khoản và chia sẻ vẫn giữ nguyên phạm vi thu thập và tiết lộ riêng của chúng.

Các tùy chọn thiết kế/biểu đồ được chia sẻ được cố định trong các tệp xuất mới của cuộc trò chuyện/tài khoản và bản xem trước chia sẻ tài khoản. Cài đặt ngôn ngữ và quyền riêng tư của tài khoản/chia sẻ vẫn độc lập; các ghi chú riêng tư về vụ việc và kiểm tra không được sao chép vào các tệp xuất này. Các báo cáo về tài khoản và chia sẻ vẫn ở định dạng HTML được bảo vệ bởi bản kê khai lưu trữ đã ký. Nhật ký, bộ công cụ bàn giao nhật ký thu gọn và bộ công cụ trò chuyện đơn lẻ cũng cung cấp các tệp PDF đã ký.

### Các biểu đồ thể hiện những gì

Hoạt động nhật ký và bản đồ nhiệt tính số lượng **các quan sát** mới, lịch sử, đã khôi phục, đã chỉnh sửa, đã xóa và thiếu khi kiểm tra lại, theo thời gian quan sát của bộ thu thập theo múi giờ UTC. Các tín hiệu kiểm tra kết nối và biên nhận tệp đính kèm bị loại trừ. Xếp hạng người tham gia chỉ tính các quan sát tin nhắn mới, lịch sử và đã khôi phục: người gửi không được coi là người chỉnh sửa hoặc người xóa. Các quan sát lặp lại có thể mô tả cùng một tin nhắn Telegram.

Phân tích nhật ký lưu giữ số lượng theo loại, tham chiếu bản ghi đầu tiên/cuối cùng và tệp nguồn ` `events.jsonl`` với mã SHA-256. Các số liệu bao gồm giá trị chính xác trong HTML và PDF. Các khoảng thời gian hàng ngày sẽ chuyển sang đơn vị tháng sau khi vượt quá 366 ngày được ghi lại; các biểu đồ kết hợp các khoảng này thành tối đa 36 khoảng có độ rộng bằng nhau. Hơn 100.000 định danh riêng biệt hoặc 1.200 mốc tháng khiến biểu đồ liên quan không khả dụng, trong khi tổng số liệu chính xác vẫn có sẵn.

Biểu đồ chụp nhanh và chia sẻ tài khoản chỉ tính các hàng tin nhắn không phải dịch vụ được bao gồm, dựa trên thời gian tin nhắn được ghi lại. Các số liệu tổng hợp về chia sẻ được tính toán sau khi che giấu thông tin và lọc dữ liệu. Các biểu đồ này sử dụng tối đa 90 khoảng thời gian ngày theo UTC có độ rộng bằng nhau và giữ lại tối đa 10.000 giá trị nhóm; các số liệu vượt quá được khai báo rõ ràng và đối chiếu. Khoảng thời gian cuối cùng có thể ngắn hơn. Các ngày tháng không xác định hoặc không chính xác sẽ không được đưa vào biểu đồ thời gian.

Một khoảng trống có nghĩa là không có quan sát nào được bao gồm; tham khảo phạm vi bao phủ để xác định các khoảng trống. Các biểu đồ này mô tả hoạt động đã lưu. Người gửi không xác định vẫn là một danh mục riêng biệt, và mỗi lần kiểm tra được báo cáo riêng lẻ.

Khi được bao gồm, tệp `analytics.json` được bảo vệ bởi các hàm băm tệp đã ký của kho lưu trữ. Tệp `report.json` của nhật ký nhúng cùng một tổng hợp đã chọn. Xác minh chữ ký phát hiện các byte bị thay đổi. Để kiểm tra các con số, hãy tính lại các tổng hợp nhật ký bằng `report_analytics.Analytics` và `selected`, hoặc các tổng hợp ảnh chụp nhanh bằng `snapshot_analytics.collect` và `project`.

### Các chỉ số bất thường

**Xem trước.** Báo cáo bằng chứng bổ sung phần **Chỉ số bất thường** được tính toán bởi các bộ xử lý đã đăng ký (`tgwitness/metrics/`, một tệp cho mỗi chỉ số). Báo cáo liệt kê tên của mọi bộ xử lý đã chạy kèm theo phiên bản của nó, và hiển thị phương pháp tính toán dưới bảng dữ liệu của nó, để quá trình tính toán có thể được lặp lại từ `events.jsonl` với `tgwitness.metrics.run`.

| Bộ xử lý | Nội dung hiển thị |
| --- | --- |
| `first_time_posters_over_time` v1 | Số người đăng bài lần đầu và số tin nhắn mỗi ngày theo giờ UTC. Một cờ cảnh báo yêu cầu ít nhất năm người đăng bài lần đầu và gấp ba lần giá trị trung vị của số người này, với khối lượng tin nhắn tối đa bằng 1.5 lần giá trị trung vị của khối lượng tin nhắn. Mức cơ sở sử dụng ít nhất bảy ngày quan sát trong vòng 14 ngày lịch trước đó, sau bảy ngày khởi động. |
| `service_vs_message_ratio` v1 | Số tin nhắn đã lưu riêng biệt cho từng cuộc trò chuyện và phần được sử dụng bởi các tin nhắn dịch vụ. Tài liệu này mô tả hệ thống đánh số; nó không giải thích về một số cụ thể nào đó bị thiếu. |
| `join_leave_per_month` v1 | Số lượt tham gia, rời khỏi, xóa hoặc cấm mỗi tháng, mỗi người, mỗi cuộc trò chuyện, mỗi thay đổi và mỗi ngày. |
| `pinned_per_month` v1 | Số lượng tin nhắn dịch vụ được ghim, thông báo gỡ ghim, cũng như tin nhắn được ghim được thêm vào hoặc xóa đi giữa các bản chụp trạng thái cuộc trò chuyện, tính theo tháng. |

**Tham số → Chỉ số báo cáo** chọn bộ xử lý và số hàng hiển thị, bao gồm cả trong các báo cáo đã lọc. Các bảng hàng ngày và hàng tháng hiển thị các hàng gần đây, các bảng chia sẻ dịch vụ xếp hạng các cuộc trò chuyện theo số lượng tin nhắn đã lưu. Tổng số bao gồm mọi hàng.

Từ bản sao nguồn, hãy xây dựng tất cả tám mẫu thiết kế được liệt kê ở trên dựa trên cùng một tạp chí hư cấu:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Mở tệp `index.html` kết quả để so sánh các báo cáo HTML đầy đủ, các tệp PDF đã ký và các tệp ZIP. Mỗi thiết kế đều sử dụng cùng một nhật ký nguồn. Sử dụng một thư mục đầu ra mới cho mỗi lần chạy để các ví dụ đã ký trước đó được bảo toàn.

![Hồ sơ HTML giả định](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

Trang HTML mở đầu bằng trang bìa vụ án và các số liệu chính. Bản đồ bằng chứng được đánh số liên kết đến từng phát hiện, các sự kiện hỗ trợ, giới hạn và đánh giá độc lập. Các bản ghi có thể tìm kiếm và các tham chiếu bản ghi ổn định vẫn có sẵn trong trình xem ngoại tuyến. Thiết kế thích ứng với màn hình hẹp, cả các chủ đề và trình duyệt không sử dụng JavaScript.

Tệp PDF đã ký có trang bìa A4 riêng biệt, mã tham chiếu báo cáo và mã QR, phần tóm tắt chính, bản đồ bằng chứng, các kết luận được đánh số và dấu trang tài liệu. Các tiêu đề trên đầu và chân trang giúp nhận diện báo cáo. Mã QR xác định tài liệu; đây không phải là kết quả xác minh độc lập. Các bản in từ trình duyệt là riêng biệt so với tệp PDF đã được ký số này.

Dòng thời gian quan sát hiển thị các khoảng thời gian quan sát được ghi lại và các sự gián đoạn trên cùng một trục UTC. Khoảng trống không được coi là phạm vi bao phủ; các bảng chi tiết giữ nguyên các khoảng thời gian chính xác. Tệp ZIP chứa các báo cáo có thể đọc được, tệp JSON đã ký, hồ sơ nguồn và hướng dẫn xác minh.

Tạo một hồ sơ mới, hư cấu bằng tiếng Anh/tiếng Nga/tiếng Đức với môi trường phát triển đã được cài đặt:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Mỗi thư mục ngôn ngữ chứa các tệp `report.html`, `report.pdf`, `report.json` và `dossier.zip`. Các thư mục mẫu hiện có sẽ không bao giờ bị ghi đè. Không sử dụng tài khoản Telegram, dịch vụ đóng dấu thời gian bên ngoài hoặc kết nối mạng để tạo ra nó.

![Ba trang đầu tiên của tệp PDF giả định đã được ký tên](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Đọc một trường hợp cụ thể

Đối với một nhật ký có 1.200 mục nhập với dấu thời gian đã được xác thực tại mục nhập thứ 1.000, báo cáo xác định có 200 mục nhập sau đó nằm ngoài giới hạn của dấu thời gian đó. Đây là giới hạn trên về sự tồn tại của một điểm kiểm tra, không phải bằng chứng về thời gian gửi của từng tin nhắn. Nếu ba tệp dấu thời gian khác không qua được quá trình xác thực hoặc không thể xác thực, chúng sẽ được tính riêng và không thể đưa ra kết luận khẳng định.

Một dấu thời gian có thể sử dụng phải đáp ứng tất cả các kiểm tra sau: dấu ấn của nó khớp với điểm kiểm tra, chữ ký của nó được liên kết với một gốc TSA đáng tin cậy tại thời điểm đóng dấu, và chữ ký, khóa, số lượng và đầu của điểm kiểm tra phải khớp chính xác với tiền tố nhật ký. Chỉ phân tích cú pháp dấu thời gian hoặc có biên nhận OTS là chưa đủ. Người đọc phải tự chọn gốc TSA đáng tin cậy và lặp lại quá trình xác minh. OTS cần có kiểm tra xác nhận Bitcoin riêng.

| Trạng thái báo cáo | Ý nghĩa |
| --- | --- |
| Đã kiểm tra trong quá trình xuất | Trình xuất đã thực hiện kiểm tra như đã nêu; vẫn cần thực hiện lại một cách độc lập. |
| Đã ghi lại; cần xem xét | Quan sát cơ bản hoặc tuyên bố của người vận hành được ghi lại; đây không phải là xác nhận độc lập. |
| Không bao gồm trong bản dịch này | Nội dung này không có bằng chứng hỗ trợ cho tuyên bố này. Nó cũng không khẳng định rằng không có thông tin tương tự ở nơi khác. |
| Chưa được kiểm tra độc lập | Báo cáo không cung cấp kết quả xác minh độc lập. |
| Thiếu hoặc không có sẵn | Thiếu tài liệu hoặc bước kiểm tra bắt buộc, không đầy đủ hoặc không thành công. |

Kiểm tra từng mục riêng biệt, cùng với phạm vi thu thập đã ghi lại.

## Những yếu tố nào một cấu hình mạnh mẽ phải bảo toàn

1. Trước khi dựa vào quá trình thu thập, hãy lưu giữ dấu vân tay khóa của người thu thập thông qua một kênh đáng tin cậy riêng biệt. So sánh tham chiếu đó với khóa ký của tệp xuất.
2. Giữ lại các điểm kiểm tra có dấu thời gian độc lập và, nếu có sử dụng, một nhật ký chứng kiến nằm ngoài sự kiểm soát hành chính của bộ thu thập. So sánh chúng với nhật ký đã xuất để kiểm tra các ranh giới trước đó của nó.
3. Phạm vi thu thập bản ghi, các khoảng trống, bộ lọc, giới hạn và các thay đổi trong quá trình thu thập. Giải thích các khoảng thời gian bị thiếu liên quan đến khiếu nại thực tế, đồng thời phân biệt rõ ràng các ID tin nhắn không được ghi nhận, thông báo xóa và các lần kiểm tra lại không thành công.
4. Giữ nguyên các tệp ZIP gốc và các giá trị băm của chúng. Ghi lại từng người nắm giữ, lần chuyển giao, ngày tháng và mục đích. Giữ lại các tuyên bố của người vận hành được ghi nhận và các ghi chú vụ việc kèm theo chúng.
5. Đối với các máy ảo (VM) bí mật, cần bảo toàn và xác minh độc lập các thông tin sau: trích dẫn, thách thức, chuỗi chứng chỉ Intel, các phép đo, nguồn chính xác và điều kiện xử lý khóa. Giữ lại kết quả xác minh chứng nhận cùng với các bằng chứng đã được xem xét.

Xem [Phạm vi xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope) để biết các kiểm tra về việc thu thập, tính toàn vẹn của kho lưu trữ, thời gian và phạm vi thu thập trong từng chế độ.

## Xem xét của người nhận

Sử dụng bản cài đặt đáng tin cậy của TgWitness và dấu vân tay được thu thập độc lập:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

Tệp ZIP chứng cứ phải đến từ một nguồn đáng tin cậy độc lập; giữ nguyên khóa và nguồn gốc của nó. Giữ nguyên các lệnh, phiên bản công cụ, kết quả đầu ra, các giá trị băm đầu vào đã được kiểm tra và các câu hỏi chưa được giải quyết. Xác minh Beacon là một quá trình kiểm tra trực tuyến riêng biệt; trình hiển thị báo cáo không bao giờ liên hệ với bất kỳ dịch vụ nào chỉ để hiển thị báo cáo.

Đối với tranh chấp về một tin nhắn cụ thể, hãy trích dẫn tham chiếu lưu trữ, tệp có thẩm quyền và tham chiếu bản ghi, sau đó mô tả khoảng thời gian liên quan, các khoảng trống trong phạm vi, việc lựa chọn và tài liệu chứng thực. Đối với bản sao chia sẻ, cũng cần xem xét quá trình chuyển đổi đã ghi lại và các tham chiếu của nó đến kho lưu trữ nguồn. Các bộ lọc riêng tư và bản đồ nhận dạng nằm ngoài phạm vi đánh giá công khai.

Việc xác minh tệp PDF đã ký sẽ phát hiện các thay đổi đối với các byte được bảo vệ. Giữ lại tệp kỹ thuật số gốc và kết quả xác minh cùng với bất kỳ ảnh chụp màn hình hoặc bản in nào.
