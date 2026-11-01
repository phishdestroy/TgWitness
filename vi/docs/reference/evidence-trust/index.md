# Bằng chứng và sự tin cậy

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence-trust/

Những gì các tệp xuất, video, kho lưu trữ web và bản ghi đã ký có thể xác lập, cũng như cách thiết bị thu thập ảnh hưởng đến độ tin cậy của chúng.

Việc xuất dữ liệu, chụp màn hình hoặc ghi lại có thể là bằng chứng hữu ích. Độ tin cậy của chúng phụ thuộc vào cách chúng được thu thập, bảo quản và xác minh. **Một hàm băm hoặc chữ ký hợp lệ kiểm tra tài liệu đã lưu; nó không tự nó chứng minh rằng thiết bị thu thập đã nhận được nội dung nguồn chính xác.** Ranh giới này cũng áp dụng cho TgWitness.

Hướng dẫn này tách biệt việc xác minh kỹ thuật khỏi đánh giá pháp lý. Tài liệu sản phẩm và các quy định pháp lý dưới đây đã được rà soát vào ngày 1 tháng 11 năm 2026; so sánh của Hunchly mô tả tài liệu đã công bố của họ, không phải một cuộc kiểm toán sản phẩm mới.

## Khi yếu tố tin cậy được đưa vào quá trình thu thập

Sơ đồ quy trình · Tài khoản và dịch vụ Telegram → Ứng dụng khách, trình duyệt và hệ điều hành; Ứng dụng khách, trình duyệt và hệ điều hành → Xuất, quay video hoặc chụp màn hình trang; Xuất, quay video hoặc chụp màn hình trang → Hashes và chữ ký của bộ thu thập; Hashes và chữ ký của bộ thu thập → Hash được lưu giữ bởi một bên độc lập · Tài khoản và dịch vụTelegram · Ứng dụng khách, trìnhduyệt và hệ điều hành · Xuất, quay video hoặcchụp màn hình trang · Hashes và chữ ký củabộ thu thập · Hash được lưu giữ bởimột bên độc lập

**Sơ đồ dưới dạng văn bản**

1. Tài khoản và dịch vụ Telegram → Ứng dụng khách, trình duyệt và hệ điều hành
2. Ứng dụng khách, trình duyệt và hệ điều hành → Xuất, quay video hoặc chụp màn hình trang
3. Xuất, quay video hoặc chụp màn hình trang → Hashes và chữ ký của bộ thu thập
4. Hashes và chữ ký của bộ thu thập → Hash được lưu giữ bởi một bên độc lập

Mô hình mối đe dọa ở đây giả định rằng kẻ tấn công hoặc người vận hành có thể thay đổi môi trường thu thập trước khi bằng chứng được lưu lại. Đây là một phân tích có điều kiện, không phải lời khẳng định rằng một thiết bị hoặc sản phẩm cụ thể nào đó đã bị xâm phạm.

Một ứng dụng khách chính thức và kết nối được mã hóa giúp bảo vệ việc sử dụng bình thường. Chúng không làm cho hệ điều hành, trình duyệt hoặc màn hình xung quanh trở nên đáng tin cậy một cách độc lập. Nếu nội dung bị thay thế sau khi giải mã nhưng trước khi ghi lại, người xuất có thể lưu nó một cách chính xác và người ký có thể ký nó một cách chính xác. Cả hai hoạt động này đều không cần thuật toán băm bị hỏng hoặc chữ ký giả mạo.

Một video được quay trên cùng một thiết bị có thể ghi lại cùng một nội dung hiển thị đã được thay thế. Một camera riêng biệt có thể xác nhận những gì màn hình hiển thị, nhưng màn hình hiển thị một mình không xác thực những gì Telegram cung cấp. Tương tự, HTML, JSON, ảnh chụp màn hình và nhật ký trình duyệt khớp nhau từ một môi trường được kiểm soát có thể có cùng một lỗi. Sự khớp nhau của chúng là bối cảnh hữu ích; nó không tự động là bằng chứng xác nhận độc lập.

## Mỗi hình thức bằng chứng đóng góp những gì

| Nội dung | Đóng góp hữu ích | Câu hỏi còn lại |
| --- | --- | --- |
| Xuất từ Telegram Desktop | Các cuộc trò chuyện có thể đọc được hoặc máy đọc được và các phương tiện truyền thông được chọn lọc | Ai đã kiểm soát các tệp khách hàng và tệp xuất, và những gì đã có sẵn hoặc bị loại trừ? |
| Ảnh chụp màn hình hoặc ghi lại màn hình | Bối cảnh hiển thị, trình tự các hành động và cách trình bày | Bản trình bày có phản ánh trung thực nguồn gốc và những gì đã xảy ra bên ngoài bản ghi không? |
| Kho lưu trữ web cục bộ, bao gồm MHTML | Nội dung trang và các tài nguyên liên quan để kiểm tra sau này | Trình duyệt đã cung cấp những gì cho trình lưu trữ, và ai là người kiểm soát trình duyệt đó? |
| Tập tin lưu trữ có chữ ký của người thu thập | Các thay đổi đối với các byte đã ký có thể được phát hiện so với một khóa đáng tin cậy và tham chiếu được giữ lại | Ai đã kiểm soát khóa ký và dữ liệu đầu vào trước khi ký? |
| Điểm kiểm tra được lưu giữ độc lập hoặc dấu thời gian đã được xác minh | Một giá trị băm hoặc điểm kiểm tra được giữ lại để so sánh với bản nộp sau này | Những byte và ranh giới nào được bao phủ, và bên độc lập thực sự chứng thực điều gì? |

Telegram ghi chép tính năng xuất dữ liệu trên Desktop dưới dạng bản sao HTML/JSON ngoại tuyến và API Takeout như một cách để truy xuất dữ liệu tài khoản đã chọn. Các mô tả này không cung cấp chữ ký của Telegram trên tệp lưu trữ cuối cùng đã xuất để người nhận xác minh. Kết luận của chúng tôi chỉ giới hạn trong các cơ chế xuất dữ liệu được ghi chép đó; đây không phải là tuyên bố rằng bằng chứng từ Telegram không có giá trị pháp lý.[Tính năng xuất dữ liệu trên Telegram Desktop](https://telegram.org/blog/export-and-more),[API Takeout](https://core.telegram.org/api/takeout).

Sự phân biệt tương tự cũng áp dụng cho các yêu cầu nền, mục bộ nhớ đệm và nhật ký mạng. Chúng có thể tiết lộ những mâu thuẫn và giúp xác thực việc thu thập. Bản thân sự phức tạp của chúng không đủ để xác định ai là người tạo ra chúng. Một kho lưu trữ được vận hành độc lập hoặc hồ sơ dịch vụ thu được riêng biệt sẽ cung cấp một nguồn khác để so sánh, tùy thuộc vào các giới hạn thu thập và lưu giữ riêng của nó.

## Hunchly minh họa cùng một ranh giới

Tài liệu của Hunchly mô tả việc băm SHA-256 đối với các bản chụp MHTML, ảnh và tệp đính kèm, kèm theo xác minh băm độc lập. Tài liệu này cũng giải thích lý do tại sao một tệp đã bị thay đổi kèm theo mã băm mới tính toán có thể vượt qua so sánh đó, và chỉ ra chữ ký cùng việc xác minh nguồn là các bước kiểm tra bổ sung.[Hunchly: băm nội dung, ảnh và tệp đính kèm](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

*Hướng dẫn Bằng chứng* đã công bố của họ, phiên bản 1.0 ngày 17 tháng 10 năm 2018, mô tả các khóa GPG và chữ ký được tạo cục bộ cho các bản chụp MHTML. Tài liệu này xác định rõ ràng việc truy cập vào khóa riêng tư cục bộ là một cách để ký lại tài liệu đã được sửa đổi. Đây là một hạn chế về độ tin cậy đã được ghi nhận, không phải bằng chứng về một lỗ hổng hiện tại chưa được tiết lộ. Hướng dẫn này cũng nêu rõ Chrome thực hiện việc thu thập MHTML. Việc mô tả Hunchly là chỉ dựa vào uy tín của nhà điều tra sẽ bỏ qua các biện pháp kiểm soát kỹ thuật này.[Hướng dẫn Bằng chứng Hunchly, các mục 2–4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

Việc liệu tài liệu được thu thập bằng một sản phẩm cụ thể có được chấp nhận trong một vụ án hay không phụ thuộc vào quyết định và hoàn cảnh liên quan. Chúng tôi không đưa ra bất kỳ tuyên bố nào ở đây về tần suất các tòa án chấp nhận Hunchly hoặc TgWitness, cũng như về việc liệu sản phẩm nào có sự chấp thuận chung từ tòa án hay không.

## Những gì TgWitness bổ sung và phạm vi bảo vệ của nó dừng lại ở đâu

TgWitness ghi lại các quan sát trong một nhật ký được ký tên và liên kết, đồng thời cung cấp các tệp xuất mà người nhận có thể kiểm tra. Các điểm kiểm tra được lưu giữ, dấu thời gian và một nhân chứng riêng biệt cung cấp cho người xem xét các tham chiếu ngoài các tệp hiện tại của người thu thập. Chúng giúp phơi bày các thay đổi đối với các bản ghi đã được cam kết trước đó. Các bản ghi phạm vi và kết quả thu thập rõ ràng giúp giải thích những gì đã và chưa được ghi lại.[Định dạng bằng chứng và việc chuyển giao](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/), [phạm vi thu thập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/).

Thời điểm của một sự thay thế có thể xảy ra là rất quan trọng:

1. **Sau khi ký, nếu không có quyền truy cập vào khóa ký:** việc thay đổi một bản ghi đã ký hoặc tệp được liên kết với bản kê khai sẽ không qua được quá trình xác minh với trình xác minh đáng tin cậy và khóa tương ứng.
2. **Với khóa thu thập, sau khi một điểm kiểm tra độc lập đã được lưu giữ:** một nhật ký thay thế có thể có các chữ ký mới hợp lệ, nhưng tiền tố bị thay đổi sẽ không đáp ứng so sánh với điểm kiểm tra trước đó. Một điểm kiểm tra chỉ được lưu giữ trên cùng một thiết bị được kiểm soát có thể được thay thế cùng với nhật ký. Các bản ghi nằm ngoài ranh giới đã lưu giữ cần có phạm vi bảo hiểm riêng.
3. **Trước khi một điểm kiểm tra bao gồm một quan sát được lưu giữ độc lập:**dữ liệu đầu vào sai có thể được ký và neo thành công, bao gồm cả các bản ghi mới được thêm vào sau một điểm kiểm tra trước đó. Điểm kiểm tra hoặc dấu thời gian kết quả vẫn bao gồm các bản ghi sai đó; nó không xác nhận tính đúng đắn của chúng.

Một nhân chứng TgWitness nhận các điểm kiểm tra đã được ký bởi người thu thập; nó không độc lập đọc cuộc trò chuyện Telegram cơ bản. Khóa và các bản ghi được lưu giữ của nó phải được tin cậy riêng biệt. Khi toàn bộ nhật ký được gửi phải được chứng thực, hãy sử dụng[quy trình chuyển giao yêu cầu ranh giới xuất cuối cùng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/#require-a-witnessed-export-boundary). Một lần kiểm tra tính toàn vẹn thông thường vẫn có thể báo cáo phần cuối chưa được chứng thực.

Một phản hồi RFC 3161 đã được xác minh có thể chứng minh rằng một điểm kiểm tra tồn tại vào thời điểm do cơ quan có thẩm quyền công bố. Nó không xác định thời điểm một tin nhắn Telegram được gửi hoặc liệu nội dung của nó có đúng sự thật hay không. Một yêu cầu đã chuẩn bị sẵn hoặc tệp phản hồi được đính kèm một mình là không đủ. Khi xác minh việc xuất dữ liệu với `tgwitness.verify`, việc kiểm tra các chữ ký TSA được đính kèm yêu cầu một CA được tin cậy rõ ràng thông qua `--tsa-ca`. Biên lai OpenTimestamps cần có xác minh độc lập `ots verify`, kèm theo việc nâng cấp bằng chứng khi cần thiết. [Quy trình đóng dấu thời gian](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

Trong [quá trình thu thập GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), một trình chạy được lưu trữ tạm thời sẽ thu thập các tin nhắn. Chứng thực liên kết kho lưu trữ với quy trình làm việc đã được phê duyệt. Chế độ này vẫn tin tưởng vào GitHub, phần mềm và các phụ thuộc đã được phê duyệt, trình trợ giúp/trình duyệt và đường hầm. Đây không phải là phần cứng bảo mật, chữ ký Telegram hay bằng chứng rằng không ai truy cập vào máy chủ. Biên nhận chạy được ký cục bộ cũng là một kết quả đo lường tự báo cáo, không phải là chứng thực phần cứng.

## Tính pháp lý phụ thuộc vào cơ sở

Bốn câu hỏi cần được phân biệt rõ ràng: liệu mục đó có đúng như những gì được mô tả hay không, liệu các byte được gửi có khớp với bản ghi được lưu giữ hay không, liệu nội dung có hỗ trợ các sự kiện được tuyên bố hay không, và liệu các quy tắc áp dụng có cho phép sử dụng nó hay không. Một kiểm tra mật mã chỉ giải quyết một phần của nền tảng đó.

Trong các thủ tục liên bang của Hoa Kỳ, Quy tắc 901 quy định các phương thức xác thực bằng chứng, bao gồm lời khai của nhân chứng có kiến thức và bằng chứng về quy trình hoặc hệ thống. Quy tắc 902(13) và 902(14) quy định các phương thức chứng nhận đối với một số hồ sơ và bản sao điện tử, kèm theo các yêu cầu thủ tục. Các ghi chú của ủy ban phân biệt việc xác thực với các vấn đề như lời khai gián tiếp, tính liên quan và việc quy thuộc. Một chữ ký phần mềm đơn thuần không phải là chứng nhận của người có thẩm quyền được mô tả tại đó.[Quy tắc Bằng chứng Liên bang 901](https://www.law.cornell.edu/rules/fre/rule_901),[Quy tắc Bằng chứng Liên bang 902](https://www.law.cornell.edu/rules/fre/rule_902).

Khi Luật Bằng chứng của Canada được áp dụng, Điều 31.1 quy định về việc xác thực các tài liệu điện tử. Điều 31.2 liên kết nguyên tắc bằng chứng tốt nhất với tính toàn vẹn của hệ thống hoặc một giả định áp dụng; Điều 31.3 quy định các trường hợp áp dụng giả định về tính toàn vẹn. Đây là các điều kiện chứng cứ được định nghĩa, không phải là giả định chung rằng bất kỳ nhà điều tra có giấy phép hoặc sản phẩm thương mại nào cũng là không thể sai lầm. [Luật Bằng chứng Canada, Điều 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Các ví dụ này không xác định tính chấp nhận được tại một khu vực pháp lý khác hoặc trong một trường hợp cụ thể. Các kiểm tra kỹ thuật nên được áp dụng nhất quán đối với tài liệu hỗ trợ hoặc phản bác một cáo buộc. Hướng dẫn này không khẳng định rằng bằng chứng của bên công tố thường dễ được chấp nhận hơn bằng chứng của bên bào chữa.

## Chuẩn bị một bản ghi mà người khác có thể đánh giá

- Mô tả tài khoản, thiết bị thu thập, người vận hành, phiên bản phần mềm, quyền truy cập, phạm vi đã chọn và khoảng thời gian thu thập. Ghi lại các sự gián đoạn và khả năng bị xâm phạm thay vì coi việc kiểm tra chữ ký thành công là bằng chứng thiết bị sạch.
- Giữ nguyên các gói ban đầu và ghi lại các lần chuyển giao, các giá trị băm và nguồn thời gian. Lưu giữ dấu vân tay khóa và các điểm kiểm tra thông qua một kênh đáng tin cậy riêng biệt. Xác minh phạm vi bao phủ thực tế của nhân chứng hoặc dấu thời gian trước khi mô tả nó trong báo cáo.
- Tìm kiếm bằng chứng xác nhận độc lập phù hợp với tuyên bố: hồ sơ của một người tham gia khác, bản ghi độc lập hoặc hồ sơ dịch vụ thu được hợp pháp. Giải thích tính độc lập và các hạn chế của chúng; sự trùng khớp giữa các bản sao thôi là chưa đủ.
- Giữ nguyên bối cảnh liên quan. Xác định các tệp bị bỏ qua, lịch sử không khả dụng và các phần bị che giấu. Chuẩn bị một [bản tiết lộ tối giản riêng biệt](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)khi cần thiết, và mô tả các biến đổi của nó mà không trình bày nó như bản gốc đầy đủ.
- Cung cấp cho người nhận hướng dẫn xác minh và các tài liệu cần thiết cho các kiểm tra đó. Giữ cho các quan sát, phát hiện kỹ thuật và kết luận của nhà phân tích có thể phân biệt được.

Đối với một lần chuyển giao cụ thể, hãy nêu rõ băm lưu trữ, khóa đáng tin cậy, kết quả xác minh và ranh giới chính xác được bao phủ từ bên ngoài. Mô tả tính xác thực của nguồn, nguồn gốc tài khoản, tính đầy đủ và các kết luận pháp lý một cách riêng biệt. Điều này cung cấp cho người kiểm duyệt tiếp theo các tuyên bố cụ thể để xem xét.
