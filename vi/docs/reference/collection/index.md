# Cách thức thu thập dữ liệu

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/

Phạm vi quan sát, cập nhật trực tiếp, kiểm tra lại, tệp đính kèm, các hành động của người dùng và ý nghĩa của “khoảng trống”, được ghi lại theo từng bản ghi.

TgWitness ghi lại những gì mà một tài khoản Telegram được kết nối quan sát được. Nhật ký này lưu giữ những quan sát đó, trình tự của chúng cũng như bối cảnh đi kèm. Công cụ này không suy luận các hành động không được quan sát thấy từ một tin nhắn bị thiếu hoặc từ việc tài khoản đang được kết nối.

## Từ quá trình đăng nhập đến sổ ghi chép

Sơ đồ quy trình · Xác thực tài khoản người dùng → Chọn các nhóm và kênh có thể truy cập; Chọn các nhóm và kênh có thể truy cập → Lưu cài đặt sự kiện và tệp đính kèm; Lưu cài đặt sự kiện và tệp đính kèm → Bắt đầu quan sát; Bắt đầu quan sát → Nhận thông tin cập nhật từ ứng dụng khách đang hoạt động; Nhận thông tin cập nhật từ ứng dụng khách đang hoạt động → Áp dụng chính sách về nguồn và sự kiện; Áp dụng chính sách về nguồn và sự kiện → Thêm một ghi chú có chữ ký; Thêm một ghi chú có chữ ký → Xem lại hoặc xuất sổ nhật ký; Thêm một ghi chú có chữ ký → Xử lý mọi tệp đính kèm đang chờ xử lý; Xử lý mọi tệp đính kèm đang chờ xử lý → Thêm kết quả tải xuống · Xác thực tài khoảnngười dùng · Chọn các nhóm và kênhcó thể truy cập · Lưu cài đặt sự kiện vàtệp đính kèm · Bắt đầu quan sát · Nhận thông tin cậpnhật từ ứng dụng kháchđang hoạt động · Áp dụng chính sách vềnguồn và sự kiện · Thêm một ghi chú cóchữ ký · Xem lại hoặc xuất sổnhật ký · Xử lý mọi tệp đính kèmđang chờ xử lý · Thêm kết quả tải xuống

**Sơ đồ dưới dạng văn bản**

1. Xác thực tài khoản người dùng → Chọn các nhóm và kênh có thể truy cập
2. Chọn các nhóm và kênh có thể truy cập → Lưu cài đặt sự kiện và tệp đính kèm
3. Lưu cài đặt sự kiện và tệp đính kèm → Bắt đầu quan sát
4. Bắt đầu quan sát → Nhận thông tin cập nhật từ ứng dụng khách đang hoạt động
5. Nhận thông tin cập nhật từ ứng dụng khách đang hoạt động → Áp dụng chính sách về nguồn và sự kiện
6. Áp dụng chính sách về nguồn và sự kiện → Thêm một ghi chú có chữ ký
7. Thêm một ghi chú có chữ ký → Xem lại hoặc xuất sổ nhật ký
8. Thêm một ghi chú có chữ ký → Xử lý mọi tệp đính kèm đang chờ xử lý
9. Xử lý mọi tệp đính kèm đang chờ xử lý → Thêm kết quả tải xuống

Việc ủy quyền, quyền truy cập vào nguồn dữ liệu, bộ thu thập đang hoạt động và việc truyền tải đầy đủ là những vấn đề riêng biệt. Việc đăng nhập thành công không đồng nghĩa với việc được cấp quyền truy cập vào mọi nhóm. Việc kết nối kênh truyền tải không đảm bảo rằng mọi bản cập nhật liên quan đều đã được nhận.

## Phạm vi giám sát: các cuộc trò chuyện được chọn, một thư mục hoặc toàn bộ tài khoản

Nguồn → **Phạm vi quan sát** quyết định những cuộc trò chuyện nào sẽ được không gian làm việc ghi lại.

| Chế độ | Ghi lại | Các cuộc trò chuyện mới |
| --- | --- | --- |
| Các cuộc trò chuyện được chọn (mặc định) | Chỉ các cuộc trò chuyện mà quý vị thêm vào thủ công | Không bao giờ được thêm tự động |
| Thư mục Telegram | Các cuộc trò chuyện trong một trong các thư mục của tài khoản: bao gồm các cuộc trò chuyện được liệt kê theo tên, cộng với các danh mục của thư mục (liên hệ, không phải liên hệ, nhóm, kênh, bot), trừ đi các cuộc trò chuyện bị loại trừ và, nếu thư mục có ghi rõ, các cuộc trò chuyện đã được lưu trữ | Các cuộc trò chuyện phù hợp sẽ được thêm vào ngay khi chúng trở nên hoạt động; các cuộc trò chuyện mà quý vị thêm vào thư mục trong Telegram sẽ được hệ thống thu thập trong vòng một giờ |
| Toàn bộ tài khoản | Mọi cuộc trò chuyện mà tài khoản này tiếp nhận | Mọi cuộc trò chuyện, nhóm, cuộc trò chuyện riêng tư hoặc bot mới đều được thêm vào ngay khi có bản cập nhật đầu tiên |

- **Các loại nguồn** (kênh, nhóm, cuộc trò chuyện riêng tư, bot) giúp thu hẹp phạm vi ở chế độ thư mục và chế độ toàn tài khoản. Các cuộc trò chuyện được chọn có thể thuộc bất kỳ loại nào, bao gồm cả cuộc trò chuyện riêng tư và bot.
- **Các cuộc trò chuyện bị loại trừ** sẽ không bao giờ được ghi lại, ở bất kỳ chế độ nào. Trong chế độ theo thư mục và toàn bộ tài khoản, việc chọn *“Loại trừ”* và *“Xóa”* trên một nguồn sẽ đưa nguồn đó vào danh sách này, do đó phạm vi ghi lại sẽ không thêm lại nguồn đó nữa. Việc chọn lại cuộc trò chuyện bằng tay (trong phần Nguồn hoặc từ danh sách Cuộc trò chuyện) sẽ loại bỏ nó khỏi danh sách. Danh sách có thể chứa tối đa 5.000 cuộc trò chuyện; nếu vượt quá con số này, *thao tác Xóa* sẽ bị từ chối và thay vào đó, cuộc trò chuyện có thể được tạm dừng.
- **Các hành động của chính tài khoản** (mặc định là bật): các tin nhắn mà tài khoản này gửi đi, các thao tác chỉnh sửa và các lần nhấn phím trên bàn phím trả lời. Khi tắt tính năng này, các tin nhắn gửi đi và các thao tác chỉnh sửa sẽ bị bỏ qua.
- Việc chuyển sang một thư mục hoặc toàn bộ tài khoản sẽ yêu cầu xác nhận: các chế độ này ghi lại các cuộc trò chuyện riêng tư và tin nhắn của bên thứ ba, và chỉ được phép thực hiện trên một tài khoản chuyên dụng. Việc xác nhận cũng như mọi thay đổi về phạm vi đều là các bản ghi `scope.changed` đã được ký điện tử.
- Các cuộc trò chuyện được thêm vào theo phạm vi sẽ xuất hiện dưới dạng các nguồn được đánh dấu là *“auto”*, được ghi lại dưới dạng `scope.applied` (khi bắt đầu và mỗi giờ) hoặc `source.discovered` (một cuộc trò chuyện mới trong quá trình theo dõi). Việc chuyển trở lại các cuộc trò chuyện đã chọn sẽ tạm dừng mọi nguồn được thêm vào tự động.

Những điều các chế độ này không thể thực hiện:

- **Các cuộc trò chuyện bí mật** được mã hóa đầu cuối giữa hai thiết bị và tuyệt đối không bao giờ được truyền đến TgWitness, dưới bất kỳ hình thức nào.
- **Không có dữ liệu nào được ghi lại khi TgWitness không hoạt động.** Sau khi khởi động lại, công cụ sẽ yêu cầu Telegram cung cấp các bản cập nhật bị bỏ lỡ và kiểm tra lại các cuộc trò chuyện; tuy nhiên, Telegram không trả về toàn bộ dữ liệu sau những lần gián đoạn kéo dài. Các báo cáo và tệp `verify.py` sẽ hiển thị những khoảng thời gian này dưới dạng khoảng trống (xem [phần phạm vi bao phủ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Ban đầu chỉ hiển thị 1.000 cuộc trò chuyện đầu tiên (giới hạn này được thiết lập trong **phần Thông số**); các cuộc trò chuyện cũ hơn sẽ được bổ sung khi chúng hoạt động trở lại. Lịch sử trước đó của một cuộc trò chuyện đã được thêm vào sẽ không được lấy về — quý vị nên tạo bản chụp nhanh lịch sử hoặc xuất toàn bộ nội dung cuộc trò chuyện khi cần thiết.
- Các điều kiện của thư mục thay đổi liên tục (bị tắt tiếng, đã đọc) sẽ không được áp dụng: các cuộc trò chuyện đó vẫn tiếp tục được theo dõi.
- **Các nút bot nhúng (callback)** được nhấn trong một ứng dụng khác sẽ không hiển thị trong phiên làm việc thứ hai; phản hồi hoặc thao tác chỉnh sửa của bot sẽ được ghi lại. Các thao tác nhấn phím trên bàn phím để trả lời sẽ được gửi dưới dạng tin nhắn đi và được gắn nhãn `button_press`.
- Càng nhiều cuộc trò chuyện đồng nghĩa với việc càng có nhiều yêu cầu. Telegram sẽ hạn chế các tài khoản có khối lượng tin nhắn mà nền tảng này coi là quá mức, đây chính là một lý do nữa để sử dụng các tài khoản chuyên dụng.

## Phạm vi và việc lựa chọn sự kiện

Mỗi không gian làm việc đều có các nguồn riêng. TgWitness không tham gia các nhóm, không chấp nhận lời mời, cũng như không tự động liệt kê từng thành viên. Các nguồn phải đã có sẵn và có thể truy cập được từ tài khoản. Khi khởi động, trình thu thập sẽ đối chiếu các nguồn đã chọn với các cuộc trò chuyện hiển thị trên tài khoản; 1.000 cuộc trò chuyện đầu tiên sẽ được kiểm tra trừ khi **mục “Tham số → Trò chuyện” trong danh sách tài khoản** có quy định khác. Nguồn không có mặt sẽ được đánh dấu **là “chưa xác nhận quyền truy cập”**, chứ không được coi là đã xóa quý vị khỏi danh sách.

| Bối cảnh | Thu thập | Tác động khi bị vô hiệu hóa |
| --- | --- | --- |
| Tin nhắn mới | Các tin nhắn đã được gửi đi thông thường | Các thao tác chỉnh sửa/xóa sau này có thể không có văn bản đã được ghi lại trước đó để so sánh. |
| Các chỉnh sửa | Cung cấp các phiên bản tin nhắn đã được chỉnh sửa | Các thay đổi ở giai đoạn trung gian sẽ không được tái tạo lại sau này. |
| Các hành động xóa | Thông báo xóa có phạm vi cụ thể và thông báo cấp tài khoản không có phạm vi cụ thể | Các thông báo xóa tin nhắn sẽ không được thêm vào sổ ghi chép. |
| Phản hồi | Các bản chụp nhanh phản ứng đã được cung cấp | Các bản cập nhật phản hồi riêng lẻ sẽ không được bổ sung. |
| Thành viên | Đã gửi các thông báo về dịch vụ thành viên và thông tin cập nhật cho người tham gia | Các quan sát liên quan đến tư cách thành viên không được bổ sung vào đây. |

Các cài đặt này áp dụng cho tất cả các nguồn đã chọn trong không gian làm việc. Vui lòng lưu biểu mẫu để áp dụng các thay đổi; các thay đổi sẽ được ghi lại kèm theo các giá trị trước và sau đã được ký xác thực. Việc vô hiệu hóa một danh mục sẽ không xóa các bản ghi trước đó. Việc kích hoạt lại danh mục này sẽ không khôi phục các bản cập nhật đã bỏ lỡ.

Các bản ghi hoạt động và các sự kiện dịch vụ nhóm khác vẫn được tách biệt với các tùy chọn này. Các tin nhắn dịch vụ thành viên có thể tạo bản ghi tin nhắn khi tính năng thành viên được kích hoạt, ngay cả khi tính năng ghi lại tin nhắn mới thông thường bị tắt. Các đối tượng Telegram được ghi lại vẫn giữ nguyên siêu dữ liệu nhúng; một tùy chọn không phải là quy tắc che giấu thông tin.

**Các hành động xóa trong các cuộc trò chuyện riêng tư và nhóm thông thường** sẽ được ghi nhận dưới dạng ID tin nhắn mà không kèm theo cuộc trò chuyện. Các cuộc trò chuyện này chia sẻ chung một chuỗi ID tin nhắn trên toàn tài khoản; do đó, khi một tin nhắn có ID đó đã được lưu trước đó, cuộc trò chuyện chứa tin nhắn đó sẽ được xác định: hành động xóa sẽ được ghi lại trong cuộc trò chuyện đó cùng với giải thích của `chat_resolution` về cách thức thực hiện. Các ID chưa từng được lưu trữ sẽ được coi là hành **vi xóa ngoài phạm vi** với nguồn gốc không xác định rõ ràng; công cụ thu thập dữ liệu sẽ không đưa ra phỏng đoán. Telegram không bao giờ tiết lộ ai là người đã xóa tin nhắn; khi tin nhắn bị xóa được gửi từ tài khoản này, bản ghi sẽ ghi nhận điều đó (`deleted_message_was_outgoing`) mà không nêu tên người xóa.

## Các hành động của chính mình

Các tin nhắn được gửi từ tài khoản đang được theo dõi sẽ được gắn nhãn `outgoing`. Việc chỉnh sửa một tin nhắn gửi đi ghi chú rằng trong các cuộc trò chuyện riêng tư và nhóm, chỉ tác giả của tin nhắn đó mới có thể chỉnh sửa, trong khi các bài đăng trên kênh có thể được chỉnh sửa bởi các quản trị viên khác. Khi một tin nhắn gửi đi lặp lại nội dung của một nút từ bàn phím trả lời được lưu gần đây nhất trong cuộc trò chuyện đó, tin nhắn này sẽ mang mã `button_press` kèm theo liên kết đến bản ghi của bàn phím đó.

Việc loại trừ các hành động do chính người dùng thực hiện cũng áp dụng cho việc kiểm tra lại nền và lịch sử cuộc trò chuyện mới tự động. Các tin nhắn gửi đi bị bỏ qua sẽ làm dịch chuyển vị trí kiểm tra lại, do đó chúng không thể chặn các tin nhắn đến sau đó. Các thao tác rõ ràng trên bảng điều khiển và các bản chụp lịch sử được yêu cầu thủ công vẫn được ghi lại.

## Chế độ điều tra: tham gia các nhóm và trao đổi với các bot

**Nguồn → Phạm vi quan sát → Chế độ điều tra** sẽ thiết lập phạm vi cho một tài khoản chuyên dụng tham gia các cuộc trò chuyện nhóm, khởi chạy các bot và gửi tin nhắn đến chúng: toàn bộ tài khoản, mọi loại nguồn, các hành động của chính tài khoản đó, cũng như hồ sơ và 200 tin nhắn hiển thị gần nhất của mọi cuộc trò chuyện hoặc bot xuất hiện. Hãy xem lại biểu mẫu và nhấn **“Lưu phạm vi”**; việc chuyển sang chế độ toàn bộ tài khoản sẽ yêu cầu xác nhận thông thường.

- **Các nút.** Các nút nằm dưới một tin nhắn sẽ được giữ nguyên cùng với tin nhắn đó và hiển thị trong **phần Trò chuyện**: các liên kết, ứng dụng web , liên kết đăng nhập, văn bản cần sao chép, dữ liệu gọi lại, truy vấn nội tuyến, yêu cầu cung cấp số điện thoại hoặc vị trí. Các liên kết được hiển thị dưới dạng văn bản và không bao giờ được bảng điều khiển mở ra. Khi một bot chỉ thay đổi các nút (ví dụ: một liên kết thanh toán mới), đó được coi là một phiên bản mới của tin nhắn, áp dụng cho cả các bản cập nhật trực tiếp lẫn các lần kiểm tra lại.
- **Các cuộc trò chuyện và bot mới.** Ở chế độ theo thư mục và toàn bộ tài khoản, **khi một cuộc trò chuyện hoặc bot mới xuất hiện**, hệ thống sẽ lưu lại ngay lập tức sau khi nó xuất hiện:

  - hồ sơ của nó dưới dạng bản ghi `source.profile`: mô tả bot và các lệnh, phần giới thiệu về người dùng, nhóm hoặc kênh, danh sách thành viên, liên kết cuộc trò chuyện và liên kết mời khi Telegram cung cấp liên kết đó;
  - các tin nhắn hiển thị gần đây nhất (tối đa 1.000 tin nhắn) dưới dạng bản chụp lịch sử được đánh dấu là `new_chat`: các tin nhắn trước đó trong một cuộc trò chuyện nhóm vừa tham gia, hoặc những gì bot đã nói trước khi hệ thống giám sát phát hiện ra cuộc trò chuyện đó. Các tin nhắn đã được lưu trữ trực tiếp sẽ không được lặp lại.

  Các cuộc trò chuyện đã có trong danh sách khi chế độ được bật sẽ được thêm vào mà không kèm theo ảnh chụp màn hình. Tính năng FloodWait sẽ tạm dừng quá trình này và tiếp tục sau đó; các sự cố sẽ được ghi lại và việc ghi lại trực tiếp cuộc trò chuyện vẫn tiếp tục. - **Hồ sơ theo yêu cầu. Cuộc trò chuyện → Hồ sơ → Lưu hồ sơ hiện** sẽ lưu lại hồ sơ hiện tại của bất kỳ nguồn nào; hồ sơ mới nhất sẽ được hiển thị phía trên các tin nhắn. - **Không hiển thị.** Các nút nhúng (callback) được nhấn trong một ứng dụng Telegram khác, cửa sổ bật lên hoặc liên kết mà bot trả lời khi người dùng nhấn vào, cũng như các liên kết mời được sử dụng trong ứng dụng khác sẽ không được truyền đến TgWitness. Những nội dung mà bot gửi hoặc chỉnh sửa sau đó sẽ được ghi lại.

### Hành động từ bảng điều khiển

**Tính năng Trò chuyện** hiện đã tích hợp một ứng dụng khách thu nhỏ sử dụng tài khoản Telegram của không gian làm việc đã chọn:

- Quý vị có thể soạn một tin nhắn dạng văn bản thuần túy hoặc chọn **“Trả lời”** bên dưới một tin nhắn đã lưu. Tin nhắn gửi đi được trả về sẽ được ghi lại ngay cả khi phạm vi ghi lại không bao gồm các cập nhật tin nhắn gửi đi.
- Nhấn **nút “Press”** bên dưới nút gọi lại hoặc nút văn bản hiện tại. Máy chủ sẽ lấy lại tin nhắn và từ chối thao tác nếu nội dung trên bàn phím khác với phiên bản đã lưu. Biên nhận gọi lại vẫn giữ nguyên văn bản cửa sổ bật lên, cờ cảnh báo và URL của Telegram; câu trả lời cũng được hiển thị bên dưới cuộc trò chuyện. Các URL vẫn là văn bản có thể chọn và không được mở tự động.
- Mở rộng **liên kết Telegram**, nhập `@username`, một liên kết `https://t.me/name` công khai, `https://t.me/+invite` / `joinchat/invite`, hoặc một liên kết bot có `?start=parameter`, rồi nhấn **Lưu bản xem trước**. Liên kết gốc và bản xem trước của Telegram sẽ được ký trước khi tham gia. **Tham gia / mở và quan sát,** sau đó tham gia nhóm/kênh hoặc mở tài khoản người dùng/bot, thêm cuộc trò chuyện làm nguồn được kích hoạt, và gửi mã `/start` đến bot, kèm theo tham số khởi động của nó. Yêu cầu tham gia đang chờ phê duyệt từ quản trị viên sẽ được ghi nhận là “đang chờ xử lý”, chứ không phải là “đã tham gia”.

Vui lòng bật tính năng **“Bắt đầu quan sát”** để ghi lại các phản hồi đến theo thời gian thực. Các thao tác trên bảng điều khiển vẫn hoạt động khi quá trình quan sát bị tạm dừng, nhưng lúc đó chỉ các phản hồi trực tiếp từ các thao tác đó mới được đảm bảo lưu lại. Các nguồn mới được thêm vào sẽ sử dụng cấu hình hồ sơ/lịch sử đã thiết lập khi quá trình quan sát đang diễn ra. Khi một nguồn bị tạm dừng, quý vị cần kích hoạt lại nguồn đó trong **phần “Nguồn”** trước khi gửi tin nhắn hoặc nhấn các nút tương ứng.

`interaction.preview`, `interaction.requested` và `interaction.result` là các sự kiện nhật ký có chữ ký thông thường được bao gồm trong các tệp xuất bằng chứng. Các yêu cầu xác định tài khoản, tin nhắn/nút hoặc bản ghi xem trước và liệu quá trình quan sát có đang chạy hay không. Các biên nhận phân biệt giữa thành công, bị từ chối, đang chờ phê duyệt và kết quả không xác định. Một yêu cầu bị gián đoạn có thể đã được gửi đến Telegram: vui lòng kiểm tra cuộc trò chuyện trước khi thực hiện hành động mới. Việc sử dụng lại ID yêu cầu sẽ truy xuất biên nhận đã lưu mà không cần lặp lại thao tác, kể cả sau khi khởi động lại. Bảng điều khiển sẽ giữ lại ID sau khi nhận được phản hồi không rõ ràng cho cùng một thao tác trong phiên trang hiện tại. Nó cũng giữ lại ID đó khi việc làm mới giao diện không thành công sau một thao tác thành công: biên nhận vẫn hiển thị, và việc nhấp lại sẽ truy xuất biên nhận đó. Các RPC gọi lại và tham gia chỉ có một lần thử; các thao tác đọc có thể thử lại sẽ giữ nguyên chính sách thử lại đã cấu hình. Việc chuyển sang cuộc trò chuyện khác ngay lập tức sẽ xóa bản nháp và mục tiêu trả lời, đồng thời vô hiệu hóa việc gửi tin nhắn cho đến khi cuộc trò chuyện mới được tải xong.

Ứng dụng khách thu nhỏ này xử lý các nút văn bản và nút gọi lại. Các ứng dụng web, yêu cầu đăng nhập/số điện thoại/vị trí, thanh toán, truy vấn nội tuyến và tệp đính kèm vẫn yêu cầu phải có ứng dụng khách Telegram; siêu dữ liệu của các nút đã lưu vẫn hiển thị. Các điều khiển mới sử dụng văn bản tiếng Anh.

## Các cấp độ kiểm tra lại

Quá trình kiểm tra lại sẽ yêu cầu Telegram cung cấp lại các tin nhắn bị bỏ sót, các thao tác chỉnh sửa và những tin nhắn mà nền tảng này không còn trả về. Các nguồn được đánh dấu bằng dấu sao là nguồn **ưu tiên**, được kiểm tra lại mỗi 15 phút theo mặc định; tất cả các nguồn còn lại được kiểm tra lại mỗi 6 giờ. Các cuộc trò chuyện được chọn ban đầu sẽ là nguồn ưu tiên, trong khi các cuộc trò chuyện được thêm vào qua thư mục hoặc toàn bộ tài khoản sẽ được coi là nguồn thông thường. Tối đa 30 nguồn được kiểm tra lại trong mỗi lần và phần còn lại sẽ chờ đến phút tiếp theo; sau khi kết nối lại, các nguồn ưu tiên sẽ được xử lý trước. Cả hai khoảng thời gian này đều được thiết lập tại Nguồn → Cài đặt ghi chép → Kiểm tra lại (giá trị 0 sẽ tắt tính năng này) và được ghi lại dưới dạng `recheck.changed`.

Các tin nhắn bị bỏ sót sẽ được lấy lại từ điểm mà lần quét trước đó dừng lại, tối đa là **số tin nhắn mới cho mỗi lần kiểm tra lại** (mặc định là 1.000) theo cài đặt **tại mục Thông số → Số tin nhắn mới** cho mỗi lần **kiểm tra lại**. Do đó, sau một khoảng thời gian ngừng hoạt động dài, quá trình kiểm tra lại sẽ lấp đầy toàn bộ khoảng trống, ngay cả khi các tin nhắn trực tiếp mới hơn khoảng trống đó đã được lưu trước. Một cuộc trò chuyện vẫn đang trong quá trình cập nhật sẽ được kiểm tra lại vào phút tiếp theo thay vì chờ đến khoảng thời gian định kỳ của nó; `recheck.completed` sẽ hiển thị `continues_after` cho đến khi quá trình hoàn tất.

Các yếu tố được so sánh bao gồm nội dung tin nhắn, các thực thể, thao tác trên bàn phím (bao gồm cả việc xóa) và nội dung/thông tin nhận dạng của tệp đính kèm. Việc thay đổi mã băm truy cập tệp hoặc tham chiếu tệp đơn thuần không được coi là một hành động chỉnh sửa, cũng như những thông tin mà Telegram tự động điền vào: quá trình tải bản xem trước liên kết, số lượt xem bài đăng, nội dung đa phương tiện trả phí được mở khóa bởi tài khoản này, hoặc biên lai hóa đơn. Mỗi phiên bản được lưu trong mục “Trò chuyện” đều có liên kết đến bản ghi nhật ký đầy đủ của nó, bao gồm cả siêu dữ liệu phương tiện.

## Lịch sử tin nhắn và nguồn gốc

Giả sử công cụ thu thập ghi nhận “Cuộc họp lúc 10:00”, sau đó thấy “Cuộc họp lúc 11:00”, và tiếp theo nhận được thông báo xóa tin nhắn. Công cụ sẽ bổ sung ba ghi nhận riêng biệt. Nội dung gốc vẫn được giữ nguyên, bản chỉnh sửa là một phiên bản riêng biệt, và thông báo ghi lại rằng đã phát hiện hành vi xóa tin nhắn.

Nếu quá trình thu thập bắt đầu sau khi phiên bản đầu tiên biến mất, thì nội dung văn bản đó sẽ không còn khả dụng. Nếu có nhiều lần chỉnh sửa xảy ra trong thời gian hệ thống ngừng hoạt động, thì chỉ những phiên bản được ghi nhận sau đó mới có thể được lưu lại. Thông báo xóa bỏ không thể khôi phục nội dung chưa từng được ghi lại.

Người gửi tin nhắn không tự động được coi là người chỉnh sửa. Telegram thường không cung cấp thông tin về người đã xóa tin nhắn hoặc thời điểm xóa chính xác. Các đối tượng không xác định vẫn giữ nguyên trạng thái ẩn danh. Các bản chụp nhanh phản hồi và cập nhật về người tham gia chỉ chứa số lượng và danh tính mà Telegram hiển thị cho tài khoản đó.

Các số thứ tự thể hiện thứ tự quan sát. Dấu thời gian UTC của bộ thu thập là thời gian theo đồng hồ địa phương của nó; dấu thời gian nguồn từ Telegram sẽ được lưu trữ riêng biệt khi có sẵn. Cả hai đều không phải là dấu thời gian đáng tin cậy độc lập.

## Các bản chụp lịch sử

Một yêu cầu chụp nhanh sẽ lấy các tin nhắn mới nhất hiện có từ một nguồn đã được kích hoạt, tối đa 500 tin nhắn cho mỗi yêu cầu. Kết quả được gắn nhãn là các quan sát lịch sử. Chúng có thể trùng lặp với dữ liệu thu thập trực tiếp, và các quan sát lặp lại sẽ được lưu giữ dưới dạng các bản ghi riêng biệt.

Các bản chụp nhanh tuân thủ chính sách đính kèm nhưng vẫn tách biệt với các chuyển đổi sự kiện trực tiếp. Chúng không khôi phục các tin nhắn đã bị xóa hoặc các phiên bản trung gian bị bỏ lỡ. Quý vị có thể yêu cầu tạo bản chụp nhanh khi quá trình đang tạm dừng; mọi tệp đính kèm được xếp hàng sẽ chờ cho đến khi quá trình quan sát bắt đầu và trình xử lý tải xuống được khởi chạy.

## Xử lý tệp đính kèm

Tính năng tải xuống tệp đính kèm được bật theo mặc định và sẽ tạm dừng khi dung lượng đĩa trống còn dưới 1 GiB. Trình thu thập sẽ thực hiện công việc quan sát tin nhắn và tải xuống cùng lúc. Công việc này giữ nguyên thông tin mô tả phương tiện gốc và chính sách về kích thước, do đó tệp đính kèm bị chỉnh sửa sau này sẽ không bị thay thế một cách âm thầm.

Quá trình tải xuống diễn ra sau khi ghi lại tin nhắn. Một lần tải xuống hoàn tất sẽ tạo ra một bản ghi `media.saved` kèm theo mã SHA-256 và số byte tương ứng. Các tác vụ bị bỏ qua, thất bại, thử lại hoặc bị gián đoạn sẽ có kết quả riêng biệt. Một tác vụ đang chờ xử lý không phải là bằng chứng cho thấy tệp đã được bảo toàn. Tệp đã hoàn tất cũng phải khớp với số byte trong mô tả tệp đính kèm ban đầu được quan sát. Phản hồi ngắn hơn hoặc dài hơn dự kiến sẽ không được ghi nhận là phương tiện truyền thông đã được bảo toàn.

Các giới hạn được thiết lập **theo từng loại**: ảnh, video, GIF và hình động, tin nhắn video dạng vòng lặp, tin nhắn thoại, nhạc và âm thanh, nhãn dán, và tệp tin. Mỗi loại có thể được tắt và có giới hạn dung lượng riêng từ 1 đến 2.000 MiB; các không gian làm việc mới bắt đầu với 20 MiB cho ảnh, 100 MiB cho video, 50 MiB cho tệp tin, âm thanh và video tròn, 20 MiB cho tin nhắn thoại và GIF, cùng 5 MiB cho nhãn dán. *Giới hạn kích thước tệp tối đa* sẽ áp dụng đồng thời cho mọi loại. Các chính sách được lưu trước khi áp dụng giới hạn theo từng loại sẽ vẫn giữ nguyên giới hạn riêng cho từng loại. Khi một loại bị tắt, hệ thống sẽ tạo ra bản ghi `media.skipped`; các tệp có kích thước không xác định hoặc vượt quá giới hạn sẽ không được tải xuống. Các tệp tin lớn sẽ được cấp tốc độ tải xuống tối thiểu 256 KiB/s. Các tác vụ vẫn tồn tại sau khi khởi động lại, nhưng các tham chiếu đã hết hạn, mất quyền truy cập hoặc tệp tin bị xóa vẫn có thể cản trở việc khôi phục. Các tác vụ hiện có sẽ giữ nguyên chính sách đã được lưu cùng với chúng.

## Tạm dừng, khóa, ngắt kết nối và khởi động lại

| Hành động hoặc điều kiện | Hiệu quả |
| --- | --- |
| Chuyển đổi không gian làm việc | Thay đổi chế độ xem bảng điều khiển; các trình thu thập khác vẫn giữ nguyên trạng thái của chúng. |
| Khóa bảng điều khiển hoặc đóng tab | Giữ cho máy chủ và quá trình giám sát tiếp tục hoạt động. |
| Tạm dừng quan sát | Tạm dừng quá trình thu thập và bảo toàn các tệp đính kèm đang chờ xử lý. |
| Vô hiệu hóa một nguồn | Tính năng này sẽ ngừng việc ghi lại theo phạm vi trong tương lai; các tác vụ phương tiện đang chờ xử lý sẽ bị tạm dừng trong thời gian tính năng này bị vô hiệu hóa. |
| Loại bỏ một nguồn | Hệ thống sẽ loại bỏ nguồn này và xóa các hồ sơ người dùng liên quan; các bản ghi đã được lưu trữ vẫn được giữ lại trong sổ nhật ký chỉ ghi thêm. Các tệp đính kèm vẫn đang chờ xử lý sẽ được ghi nhận là thất bại (`source_removed`). Trong chế độ theo thư mục và chế độ toàn tài khoản, các tệp này cũng sẽ bị loại trừ. |
| Thay đổi lộ trình kết nối | Yêu cầu tạm dừng, đóng các phiên khách hàng cũ và hủy các phiên đăng nhập chưa hoàn tất. |
| Dừng tiến trình Python | Tạm dừng tất cả các không gian làm việc; không có bất kỳ ghi nhận nào được thực hiện trong thời gian công cụ này ở chế độ ngoại tuyến. |
| Khởi động lại sau khi quan sát tích cực | Hệ thống sẽ cố gắng khôi phục phạm vi đã lưu bằng cách sử dụng phiên làm việc đã lưu. Việc tạm dừng thủ công sẽ hủy bỏ ý định đó. |

Trình thu thập ghi lại các sự cố ngắt kết nối, thử lại, lỗi, khởi động/dừng hoạt động và các tín hiệu kiểm tra kết nối. Các sự gián đoạn ngắn có thể bị bỏ sót trong quá trình kiểm tra kết nối định kỳ. Sau khi khởi động lại, các bản cập nhật bị bỏ lỡ sẽ được yêu cầu từ vị trí cập nhật đã lưu và các cuộc trò chuyện được theo dõi sẽ được kiểm tra lại định kỳ; xin tham khảo [định dạng bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#durable-collection-and-process-receipts-02). Một bản chụp nhanh cung cấp bối cảnh; nó không chứng minh rằng khoảng trống đó đã được khắc phục.

## Cách ly và xác minh tài khoản

Mỗi không gian làm việc đều có sổ nhật ký, quyền truy cập, khóa ký, chính sách và hàng đợi riêng. Chỉ khách hàng đang hoạt động của không gian làm việc đó mới có thể đóng góp các quan sát trực tiếp. Các khách hàng bị từ chối, đang chờ xử lý, bị thay thế và đang kiểm tra kết nối không thể ghi các cập nhật trực tiếp vào sổ nhật ký của không gian làm việc đó. Các tài khoản khác nhau có thể theo dõi cùng một nhóm, nhưng sổ nhật ký của họ vẫn được tách biệt.

Mỗi sự kiện bao gồm mã băm trước đó và chữ ký Ed25519. Các tệp xuất bao quát toàn bộ nhật ký không gian làm việc thông qua một số thứ tự cố định. Các bộ lọc trên bảng điều khiển không lọc dữ liệu xuất; quá trình thu thập có thể tiếp tục vượt ra ngoài ranh giới của nhật ký trong khi tệp xuất đang được chuẩn bị.

**Tính năng Xác minh Nhật ký** sẽ kiểm tra chuỗi sự kiện và các chữ ký thông qua phạm vi hiển thị. Kết quả của tính năng này sẽ bị xóa khi không gian làm việc thay đổi, và bảng điều khiển sẽ xác định các bản ghi mới được thêm vào sau khi kiểm tra. Tính năng xuất dưới dạng ZIP cũng xác minh các tệp phương tiện đã thu thập.

Một chữ ký hợp lệ xác nhận tính toàn vẹn liên quan đến khóa tin cậy, chứ không phải nguồn gốc từ Telegram hay tính xác thực của nội dung. Vui lòng lưu giữ các dấu vân tay và điểm kiểm tra một cách độc lập. Xin tham khảo [mô hình bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/), [các hoạt động hàng ngày](https://phishdestroy.github.io/TgWitness/vi/docs/reference/operations/) và [quy trình chấp nhận trực tiếp](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) để biết các yêu cầu về độ tin cậy và việc chuyển giao.
