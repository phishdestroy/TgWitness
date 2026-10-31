# Các định dạng tài khoản và phiên làm việc

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/

Đăng nhập bằng số điện thoại, mã QR hoặc khóa xác thực, nhập các phiên làm việc từ Telethon, Pyrogram hoặc Telegram Desktop, và quản lý nhiều tài khoản cùng lúc.

TgWitness đăng nhập dưới dạng tài **khoản người dùng Telegram** (không phải bot) qua giao thức MTProto, sử dụng Telethon. Mỗi tài khoản tồn tại trong **không gian** làm việc riêng (được gọi là *“workspace”* trong API và các công cụ dòng lệnh) với phiên làm việc, nguồn dữ liệu, nhật ký và khóa ký riêng.

Các tệp phiên làm việc, chuỗi phiên làm việc và Khóa xác thực là **các thông tin ủy quyền tài khoản**: bất kỳ ai sở hữu chúng đều có thể thực hiện các thao tác như chủ tài khoản đó. Chúng không chứa lịch sử tin nhắn.

> [!CẢNH BÁO] **Không nên sử dụng bất kỳ thứ gì mà quý vị không thể chấp nhận mất mát.** Chúng tôi khuyến cáo mạnh mẽ không nên kết nối các tài khoản cá nhân hoặc các tài khoản có giá trị khác, cũng như không nên tạo ID API / băm API trên một tài khoản mà quý vị coi trọng. Điều này không phải do TgWitness chưa được kiểm thử: Telegram hạn chế và cấm vĩnh viễn các tài khoản một cách khó lường — đối với khối lượng yêu cầu mà nền tảng này cho là quá mức, bất kể khách hàng hay mục đích là gì, mà không có tài liệu hướng dẫn đầy đủ. Nhiều trường hợp bị cấm là không thể đảo ngược. Hãy sử dụng các tài khoản chuyên dụng. Quá trình thử nghiệm diễn ra suôn sẻ phụ thuộc vào Telegram, không phải vào phần mềm, và không đảm bảo điều gì cho các giai đoạn sau này.

- [Tổng quan](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#at-a-glance)
- [Trước khi bắt đầu: ID API và mã băm API](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Số điện thoại](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#phone-number) · [Mã QR](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#qr-code) · [Khóa xác thực (Auth Key) + ID DC](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#auth-key--dc-id)
- [Tệp tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#pyrogram-session) · [Cặp phiên + JSON](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#telethon-stringsession) · [Tệp JSON tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-json)
- [Xác định những gì quý vị đang có](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#identify-what-you-have) · [Các định dạng không được hỗ trợ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#unsupported-formats)
- [Nhiều tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#multiple-accounts) · [Bảo vệ an toàn cho các tệp tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#keeping-account-files-safe) · [Khắc phục sự cố](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#troubleshooting)

## Tổng quan

| Những gì quý vị có | Tab **“Thêm tài khoản**” | Quý vị cũng sẽ cần |
| --- | --- | --- |
| Số điện thoại và quyền truy cập vào các mã đăng nhập của công cụ này | **Điện thoại** | Mật khẩu xác thực hai yếu tố (2FA) nếu tính năng này đã được kích hoạt |
| Telegram đang mở trên một thiết bị khác | **Mã QR** | Mật khẩu xác thực hai yếu tố (2FA) nếu tính năng này đã được kích hoạt |
| Một tệp `.session` (Telethon hoặc Pyrogram) | **Tệp tin** | Tệp JSON đi kèm (tùy chọn) dành cho cài đặt ứng dụng |
| `.session` + `.json` cùng tên | **Tệp tin** (chọn cả hai) | Thông thường không có nội dung nào khác |
| Thư mục `tdata` trên Telegram Desktop | **Tệp tin** (dạng ZIP) | Mật mã cục bộ trên máy tính để bàn (nếu đã được thiết lập) |
| Một phiên StringSession của Telethon (văn bản, `.txt`, `.tgwitness-session`) | **Tệp tin** | Không cần cặp API riêng biệt |
| Một khóa `.json` kèm theo phiên làm việc hoặc Khóa xác thực (Auth Key) | **Tệp tin** | Không cần cặp API riêng biệt |
| Một Khóa xác thực (512 ký tự hex) và số DC tương ứng | **Khóa xác thực** | ID người dùng (tùy chọn) |

TgWitness nhận diện các tệp dựa trên **nội dung** chứ không phải tên tệp. Việc đổi tên tệp sẽ không bao giờ làm thay đổi nội dung của tệp đó.

## Trước khi bắt đầu: ID API và mã băm API

Quý vị có thể đăng nhập mà không cần tạo ứng dụng API Telegram. Khi không có cặp nào được nhập, nhập khẩu hoặc đã được lưu sẵn trong không gian làm việc, TgWitness sẽ chọn một cặp ngẫu nhiên từ kho 50 cặp API công khai (`tgwitness/api_pool.py`) có sẵn trong hệ thống. Nếu Telegram từ chối một cặp khóa (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), hệ thống sẽ thử cặp tiếp theo, tối đa tám cặp cho mỗi lần đăng nhập; các cặp bị từ chối sẽ bị bỏ qua cho đến khi khởi động lại. Cặp khóa đã được sử dụng để đăng nhập sẽ được lưu cùng với tài khoản và tái sử dụng cho tài khoản đó. **Mã API** và **băm API** dùng để xác định ứng dụng với Telegram; chúng không tự thân cấp quyền truy cập cho tài khoản.

Để sử dụng ứng dụng của riêng quý vị thay thế (tài khoản đăng ký ứng dụng đó sẽ là tài khoản chịu rủi ro; xem [phần “Tại sao lại có nhóm API tích hợp sẵn?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)”):

1. Vui lòng truy cập [my.telegram.org](https://my.telegram.org) và đăng nhập bằng bất kỳ số điện thoại nào mà quý vị đang sở hữu. Mã xác minh sẽ được gửi đến ứng dụng Telegram, không phải qua tin nhắn SMS.
2. Chọn **các công cụ phát triển API**.
3. Tạo ứng dụng: bất kỳ tiêu đề và tên ngắn nào (5–32 ký tự), nền tảng **Máy tính để bàn**. Các trường URL và mô tả có thể để trống.
4. Vui lòng sao chép **App api_id** (một số) và **App api_hash** (32 ký tự thập lục phân).

Trong bảng điều khiển, phần **“API ID + Hash**” nằm ngay dưới biểu mẫu đăng nhập. Quý vị có thể dán một cặp `api_id:api_hash` duy nhất vào **ô “API ID”** và cả hai trường sẽ được điền tự động. Một cặp này có thể được sử dụng cho tất cả các tài khoản của quý vị. Sau khi đăng nhập thành công, thông tin này sẽ được lưu trữ dưới dạng mã hóa, chỉ trong không gian làm việc đó và tuyệt đối không bao giờ được gửi trở lại trình duyệt.

Có ba loại thông tin xác thực khác nhau liên quan đến vấn đề này:

| Bí mật | Mở | Địa chỉ trang web |
| --- | --- | --- |
| Mã thông báo bảng điều khiển | Bảng điều khiển web TgWitness | `panel-token.txt` trong thư mục dữ liệu, hoặc `TGWITNESS_TOKEN` |
| ID API + mã băm | Không có nội dung nào riêng lẻ; chỉ xác định ứng dụng | Cặp tài khoản tích hợp sẵn, cài đặt được nhập vào hoặc ứng dụng của riêng quý vị tại my.telegram.org |
| Xác thực tài khoản | Tài khoản Telegram | Được tạo thông qua đăng nhập bằng điện thoại/mã QR hoặc được nhập dưới dạng phiên làm việc |

Nếu cần truy cập Telegram qua máy chủ proxy, vui lòng thiết lập trước tại **mục Tài khoản → Cài đặt → Cài đặt kết nối → Thay đổi đường dẫn kết nối**.

## Số điện thoại

1. Mở **Tài khoản**, chọn tab **Điện thoại** và nhập số theo định dạng quốc tế, ví dụ: `+44 7700 900123`. Các khoảng trắng và dấu gạch ngang sẽ được tự động loại bỏ.
2. Nhấn vào **“Tiếp tục**”. Các trường API ID và Hash có thể để trống.
3. Vui lòng nhập mã mà Telegram gửi (thường được gửi đến ứng dụng Telegram; việc gửi qua tin nhắn SMS không được đảm bảo).
4. Nếu tài khoản đã bật xác thực hai bước, vui lòng nhập mật khẩu đó. Đây không phải là mã token trên bảng điều khiển và cũng không phải là mã khóa thiết bị.
5. Vui lòng kiểm tra ID tài khoản hiển thị sau khi đăng nhập, sau đó chọn các nguồn.

Mã đăng nhập và mật khẩu xác thực hai yếu tố (2FA) tuyệt đối không bao giờ được lưu trữ trên đĩa cứng.

## Mã QR

Vui lòng sử dụng tính năng này khi tài khoản đã được đăng nhập sẵn trên điện thoại hoặc máy tính khác.

1. Nhấp vào tab **Mã QR** → **Hiển thị mã QR**. Các trường API ID và Hash có thể để trống.
2. Trên thiết bị đã đăng nhập: **Cài đặt → Thiết bị → Kết nối thiết bị máy tính để bàn**, quét mã và xác nhận.
3. Vui lòng nhập mật khẩu xác thực hai yếu tố (2FA) vào TgWitness nếu Telegram yêu cầu.

Hình ảnh mã QR được tạo tại địa phương. Mã có thời hạn sử dụng; vui lòng nhấn vào **“Tạo mã QR khác”** để thử lại. Việc khóa bảng điều khiển, chuyển sang không gian làm việc khác hoặc đăng nhập bằng tài khoản khác sẽ hủy bỏ mã đang chờ xử lý.

## Khóa xác thực (Auth Key) + ID DC

Khóa xác thực (Auth Key) là khóa ủy quyền thô dài 256 byte đằng sau mỗi phiên Telegram, được biểu diễn dưới dạng **512 ký tự thập lục phân**, kèm theo số trung tâm dữ liệu **từ DC 1 đến DC 5**.

1. Tab **Khóa xác thực**. Vui lòng dán toàn bộ khóa; khóa rút gọn có chứa ký tự `…` sẽ không hoạt động.
2. Vui lòng chọn ID DC được cung cấp kèm theo khóa.
3. Quý vị có thể nhập **ID người dùng (**tùy chọn). TgWitness sẽ từ chối kết nối nếu Telegram báo cáo một tài khoản khác.
4. **Tài khoản** Press **Connect**.

Khóa xác thực (512 ký tự) không phải là mã băm API (32 ký tự). Cùng một khóa này cũng có thể được nhập dưới dạng JSON; vui lòng tham khảo [phần JSON tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-json).

## Tệp tài khoản

Mở mục **Thêm tài khoản → Tệp** và chọn tối đa **bốn tệp thuộc về một tài khoản**, tổng dung lượng **8 MiB**, sau đó nhấn **Kết nối tài khoản**.

- Các tệp tin được chuyển đổi trực tiếp **trong bộ nhớ** trên máy chủ TgWitness của quý vị. Các tệp tải lên không được lưu trữ, các tệp ZIP không được giải nén ra đĩa và không có dịch vụ bên ngoài nào được liên hệ.
- Phiên ghi chép thu được sau đó sẽ được đối chiếu với Telegram. Nếu một tệp ghi nhận ID người dùng, thì ID đó phải trùng khớp với thông tin tài khoản mà Telegram cung cấp.
- Các tệp mô tả các tài khoản khác nhau hoặc thông tin đăng nhập API khác nhau sẽ bị từ chối thay vì chỉ chọn một tài khoản duy nhất.
- Trường **“Mật khẩu hoặc văn bản phiên làm việc”** chứa trường mật khẩu cục bộ TData, một ô để dán StringSession và **đọc tệp mà không cần đăng nhập** (điền biểu mẫu mà không cần liên hệ với Telegram).

### Telethon `.session`

|  |  |
| --- | --- |
| Đây là gì | Cơ sở dữ liệu SQLite mà các công cụ dựa trên Telethon tạo ra, ví dụ như `my_account.session` |
| Được công nhận bởi | Các bảng `sessions` (cùng với `dc_id`, `server_address`, `port`, `auth_key`) và `version` = 7 hoặc 8 |
| Yêu cầu | Chính xác là một hàng phiên làm việc được ủy quyền; một cơ sở dữ liệu khép kín và hoàn chỉnh |

Trước tiên, hãy đóng chương trình đã tạo ra tệp đó. Nếu tệp `my_account.session-journal` hoặc `my_account.session-wal` vẫn tồn tại bên cạnh tệp chính, điều đó có nghĩa là cơ sở dữ liệu chưa được hoàn tất: hãy mở và đóng ứng dụng khách gốc một cách đúng quy trình. Việc xóa các tệp phụ này có thể để lại một bản sao bị hỏng.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Đây là gì | Các công cụ dựa trên Pyrogram tạo ra cơ sở dữ liệu SQLite |
| Được công nhận bởi | Bảng `sessions` với `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 hoặc 3 |
| Yêu cầu | Chỉ chấp nhận một phiên đăng nhập **của người dùng** được ủy quyền trên mạng sản xuất. Các phiên của bot và máy chủ thử nghiệm (test-DC) sẽ bị từ chối |

ID người dùng được lưu trữ sẽ được đối chiếu với hệ thống Telegram trong quá trình đăng nhập.

### Cặp phiên + JSON

Các tài khoản thường được phân phối dưới dạng hai tệp có cùng tên, ví dụ như `447700900123.session` và `447700900123.json`. Vui lòng chọn **cả hai tệp** cùng một lúc.

- Dựa trên dữ liệu JSON, TgWitness sử dụng các giao thức `app_id`/`api_id` và `app_hash`/`api_hash`, do đó quý vị thường không cần phải nhập thông tin đăng nhập API.
- Các trường khác như `phone`, `device`, `sdk`, `app_version`, `lang_pack` hoặc mật khẩu `twoFA` đã lưu sẽ bị **bỏ qua**. Nếu tài khoản có tính năng xác thực hai yếu tố (2FA), TgWitness sẽ yêu cầu xác thực.
- Một tệp JSON đơn lẻ chỉ là siêu dữ liệu. Nếu không có tệp phiên làm việc, vui lòng tiếp tục bằng cách đăng nhập qua điện thoại hoặc mã QR.

### Telegram Desktop (TData)

TData là thư mục `tdata` của ứng dụng Telegram Desktop (ứng dụng đa nền tảng từ desktop.telegram.org).

| Hệ thống | Vị trí mặc định `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (phiên bản Telegram di động: bên cạnh `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Để nhập dữ liệu:

> **Cảnh báo về phiên song song.** Việc nhập TData sẽ tái sử dụng khóa ủy quyền của Telegram Desktop; nó không tạo ra một tài khoản đăng nhập độc lập. Không được sử dụng khóa đó trên Desktop và TgWitness cùng lúc. Telegram có thể vô hiệu hóa ủy quyền với `AUTH_KEY_DUPLICATED`, khiến cả hai bản sao đều không thể sử dụng cho đến khi đăng nhập lại.
>
>
>
> Tắt hoàn toàn ứng dụng Desktop, bao gồm cả tiến trình trong khay hệ thống, và giữ bản sao đó ở trạng thái đóng trong khi TgWitness sử dụng phiên đã nhập. **Hãy thoát hoàn toàn, không đăng xuất hoặc thu hồi phiên làm việc:** việc thu hồi cũng sẽ làm bản sao đã nhập mất hiệu lực. Nếu quý vị cần cả hai ứng dụng khách cùng hoạt động, hãy đăng nhập vào TgWitness bằng điện thoại hoặc mã QR để tạo quyền xác thực riêng. Nên sử dụng một tài khoản chuyên dụng, nhưng điều này không đảm bảo rằng các khóa nhân bản sẽ an toàn khi sử dụng song song.
>
>
>
> Quy định này cũng áp dụng cho các `.session` , văn bản StringSession và mã khóa xác thực (Auth Key) dưới dạng HEX. Các ứng dụng khách khác có các phiên xác thực được tạo độc lập vẫn có thể duy trì trạng thái đã đăng nhập. Xin tham khảo [tài liệu về AUTH_KEY_DUPLICATED của Telegram](https://core.telegram.org/api/errors#406-not-acceptable).

1. Đóng hoàn toàn ứng dụng Telegram Desktop.
2. Vui lòng tạo một tệp ZIP **chỉ** chứa hai mục sau đây từ `tdata`:

   - `key_datas`
   - tệp gồm 16 ký tự kết thúc bằng `s` nằm ngay bên cạnh, thường là `D877F783D5D3EF8Cs`

   Việc nén toàn bộ thư mục cùng bộ nhớ đệm phương tiện thường vượt quá giới hạn (512 mục, 32 MiB sau khi giải nén). 3. Chọn tệp ZIP trong **phần Tệp**. Nếu Telegram Desktop có **mã thông báo cục bộ**, hãy nhập mã đó vào **ô Mã thông báo hoặc văn bản phiên** trước tiên. Đây không phải là mật khẩu xác thực hai yếu tố (2FA).

Hỗ trợ: một tài khoản cho mỗi kho lưu trữ, công nghệ lưu trữ hiện đại `key_datas`/`key_data0`/`key_data1`, mã thông báo cục bộ. Không hỗ trợ: các thư mục chứa nhiều tài khoản đã đăng nhập, các giao diện Desktop cũ, các tệp ZIP được bảo vệ bằng mật khẩu, và ứng dụng gốc riêng biệt trên macOS có tên “Telegram for macOS”.

### Telethon StringSession

Một dòng văn bản duy nhất, thường bắt đầu bằng `1` và dài khoảng 350 ký tự. Vui lòng tải tệp này dưới dạng tệp `.txt` hoặc `.tgwitness-session` (tối đa 4 KiB), hoặc dán vào phần **Mã thông báo hoặc văn bản phiên làm việc**. Chỉ chấp nhận các chuỗi Telethon; các chuỗi Pyrogram và TDLib sử dụng các định dạng khác.

### Tệp JSON tài khoản

Một đối tượng JSON, tối đa **64 KiB**, trong một tệp có phần mở rộng là **`.json`**.

| Trường (tên gọi khác) | Ý nghĩa |
| --- | --- |
| `api_id` (`app_id`) | ID ứng dụng, một số dương |
| `api_hash` (`app_hash`) | Băm ứng dụng, gồm 32 ký tự thập lục phân |
| `string_session` (`session_string`, `session`) | Văn bản Telethon StringSession, không phải tên tệp |
| `auth_key` (`auth_key_hex`) + `dc_id` | Khóa xác thực (Auth Key) đầy đủ gồm 512 ký tự và DC 1–5 |
| `user_id` (`id`) | Tùy chọn; đã được đối chiếu với Telegram trước khi lưu thông tin ủy quyền |

Nếu cả biệt danh và tên chính đều có mặt, hai tên này phải trùng khớp với nhau. Ví dụ:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

Ví dụ đầu tiên chỉ yêu cầu điền thông tin đăng nhập API; quý vị có thể đăng nhập qua số điện thoại hoặc mã QR, hoặc thêm tệp phiên làm việc. Các danh sách hàng loạt (mảng JSON chứa danh sách tài khoản) sẽ không được chấp nhận.

## Xác định những gì quý vị đang có

| Quý vị có thể thấy | Đây là | Cách sử dụng |
| --- | --- | --- |
| `*.session`; khi mở tệp này trong trình soạn thảo văn bản, phần đầu sẽ hiển thị `SQLite format 3` | Telethon hoặc Pyrogram SQLite | **Tệp tin** (được phát hiện tự động) |
| Một thư mục `tdata` chứa `key_datas` | Telegram Desktop TData | Nén hai tệp thành định dạng ZIP, sau đó là **các tệp** |
| Một dòng văn bản bắt đầu bằng `1`, khoảng 350 ký tự | Telethon StringSession | **Tệp tin** |
| `*.json` cùng với `app_id`/`app_hash` | Siêu dữ liệu đi kèm | **Các tệp tin**, cùng với phiên làm việc tương ứng |
| `*.json` kết hợp với `auth_key` hoặc `string_session` | Tệp JSON tài khoản | **Tệp tin** |
| 512 ký tự `0-9a-f` | Khóa xác thực | **Khóa xác thực** |
| 32 ký tự `0-9a-f` | Băm API | **ID API + Băm** |
| `td.binlog` hoặc `db.sqlite` từ ứng dụng TDLib | Bộ lưu trữ TDLib | Không được hỗ trợ |
| `123456789:AA…` | Mã thông báo bot | Không được hỗ trợ |

## Các định dạng không được hỗ trợ

| Định dạng | Lựa chọn thay thế |
| --- | --- |
| Bộ lưu trữ TDLib (`td.binlog`) và các tệp xuất từ TDLib | Đăng nhập bằng số điện thoại hoặc mã QR |
| **Các chuỗi** phiên làm việc của Pyrogram | Vui lòng sử dụng tệp Pyrogram `.session`, hoặc quét mã QR bằng điện thoại |
| TData với nhiều tài khoản đã đăng nhập | Vui lòng đăng xuất khỏi các tài khoản khác trên Telegram Desktop, hoặc sử dụng tệp phiên làm việc riêng của từng tài khoản |
| Mã thông báo bot | Không được hỗ trợ: TgWitness chỉ thực hiện quan sát với tư cách là một tài khoản người dùng |
| Danh sách CSV/JSON của nhiều tài khoản | Thêm một không gian làm việc cho mỗi tài khoản |
| Các phiên thử nghiệm (Test-DC) hoặc phiên bot | Vui lòng sử dụng tài khoản người dùng chính thức |

## Nhiều tài khoản

Hãy nhấn vào mã **+** bên cạnh trình chọn tài khoản, hoặc truy cập **Tài khoản → Cài đặt → Cài đặt kết nối → Không gian làm việc**, nhập tên nhãn và đăng nhập.

- Bất kỳ số lượng không gian làm việc nào, bao gồm cả không gian làm việc chính. Mỗi không gian làm việc đều có phiên làm việc, tuyến đường proxy , nguồn dữ liệu, chính sách ghi lại, sổ nhật ký, khóa ký, điểm kiểm tra và các tùy chọn xuất dữ liệu riêng biệt.
- Việc chuyển đổi không gian làm việc đang hiển thị sẽ không làm tạm dừng các không gian làm việc khác.
- Một sổ ghi chép luôn gắn liền với tài khoản đã tạo ra nó. Việc đăng nhập bằng một tài khoản khác yêu cầu phải có một không gian làm việc riêng, và một tài khoản không thể được gán cho hai không gian làm việc.
- Token bảng điều khiển chính quản lý tất cả các không gian làm việc. [Quyền truy cập được cấp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/) có thể giới hạn quyền của người khác đối với các tài khoản và cuộc trò chuyện đã chọn, kèm theo các quyền truy cập riêng biệt và giới hạn phiên làm việc.
- **Tài khoản** sẽ đổi tên một không gian làm việc và xóa một không gian làm việc đã thêm vào, cùng với phiên làm việc, nhật ký, các nguồn và khóa ký của không gian đó. Không gian làm việc chính không thể bị xóa khỏi bảng điều khiển.

### Nhập hàng loạt và nhóm tài khoản

Dùng **Tài khoản → Nhập tài khoản** để thêm nhiều tài khoản, ghép tệp theo tên gốc và xem kết quả từng lần đăng nhập. Mỗi tài khoản có không gian làm việc riêng. Nhóm có thể sao chép các thiết lập đã chọn từ mẫu mà không gộp phiên, khóa hay bằng chứng. Xem [hướng dẫn nhập và nhóm](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) và [bảng điều khiển nhóm MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Đăng xuất

**Tài khoản → Đăng xuất khỏi Telegram** (với chế độ quan sát tạm dừng) sẽ yêu cầu Telegram kết thúc phiên làm việc, do đó phiên này cũng sẽ biến mất khỏi mục **Cài đặt → Thiết bị** của tài khoản, đồng thời xóa phiên làm việc khỏi kho lưu trữ không gian làm việc. Nhật ký, các nguồn, cài đặt và khóa ký vẫn được giữ lại, và nhật ký sẽ ghi lại thao tác đăng xuất này. Không gian làm việc vẫn thuộc về tài khoản đó: chỉ có tài khoản đó mới có thể kết nối lại với nó. Nếu Telegram không phản hồi, phiên làm việc vẫn sẽ bị xóa tại đây và bảng điều khiển sẽ hiển thị thông báo tương ứng; quý vị hãy kết thúc phiên làm việc trong Telegram tại **Cài đặt → Thiết bị**.

## Chuyển đổi phiên Telethon sang chế độ ngoại tuyến

Bảng điều khiển này nhập trực tiếp các tệp `.session`. Để chuyển đổi ngoại tuyến sang tệp StringSession, hãy chạy lệnh từ thư mục dự án:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

Trình chuyển đổi này chỉ đọc tệp Telethon SQLite (tối đa 64 MiB), không bao giờ sửa đổi dữ liệu đầu vào, không thực hiện bất kỳ yêu cầu mạng nào và từ chối ghi đè lên tệp đầu ra hiện có.

## Bảo vệ an toàn cho các tệp tài khoản

- Hãy coi mọi `.session`, TData ZIP, StringSession, Auth Key và tệp JSON tài khoản như một mật khẩu. TgWitness lưu trữ thông tin ủy quyền đã nhập vào kho lưu trữ được mã hóa của mình; quý vị có thể xóa các tệp gốc sau đó.
- Không được thực hiện cùng một quy trình ủy quyền trên hai chương trình cùng lúc. Telegram có thể thu hồi ủy quyền đó (`AUTH_KEY_DUPLICATED`), và cả hai bản sao sẽ ngừng hoạt động.
- Một phiên làm việc đã hết hạn hoặc bị thu hồi không thể được khôi phục thông qua quá trình chuyển đổi. Vui lòng đăng nhập lại.

## Khắc phục sự cố

| Tin nhắn hoặc triệu chứng | Hướng dẫn thực hiện |
| --- | --- |
| *Không thể đọc phiên làm việc này. Vui lòng đóng ứng dụng gốc…* | Tệp SQLite hiện đang mở hoặc chưa hoàn tất (tệp phụ `-journal`/`-wal`). Vui lòng đóng chương trình gốc một cách đúng quy trình và sao chép lại tệp. |
| *Các lược đồ SQLite của Telethon được hỗ trợ: 7 và 8* / *Pyrogram … 2 và 3* | Tệp này được tạo ra bởi một phiên bản thư viện rất cũ hoặc không xác định. Vui lòng đăng nhập bằng số điện thoại hoặc mã QR thay thế. |
| *Chỉ hỗ trợ các phiên làm việc của người dùng được ủy quyền* | Tệp Pyrogram này thuộc về một bot hoặc mạng thử nghiệm. |
| *Kho lưu trữ TData đã vượt quá 512 mục hoặc 32 MiB* | Chỉ bao gồm các tệp ZIP `key_datas` và `D877F783D5D3EF8Cs`, không bao gồm toàn bộ thư mục. |
| *Không thể giải mã TData. Vui lòng kiểm tra mật mã cục bộ trên máy tính để bàn* | Vui lòng nhập mã mật khẩu cục bộ của Telegram Desktop vào ô **“Mật khẩu” hoặc “Văn bản phiên làm việc**”. |
| *Nhập từng tài khoản TData một* | Telegram Desktop hỗ trợ nhiều tài khoản; vui lòng tham khảo phần [“Các định dạng không được hỗ trợ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#unsupported-formats)”. |
| *Các tệp được chọn mô tả các tài khoản hoặc thông tin đăng nhập API khác nhau* | Chỉ chọn các tệp tin từ một tài khoản duy nhất. |
| *Tệp JSON không chứa thông tin xác thực hoặc ủy quyền API nào được hỗ trợ* | Vui lòng kiểm tra các tên trường trong tệp [JSON Tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-json). |
| *Chỉ bao gồm siêu dữ liệu API* | Tệp JSON không có phiên làm việc. Vui lòng thêm tệp `.session` hoặc sử dụng số điện thoại/mã QR. |
| *Mã khóa xác thực (Auth Key) dưới dạng HEX phải chứa đầy đủ 512 ký tự thập lục phân* | Khóa đã bị cắt ngắn hoặc chứa chuỗi ký tự "`…`". |
| ID tài khoản không khớp với tài khoản đã nhập | ID người dùng trong tệp này khác với thông tin mà Telegram báo cáo; tệp này thuộc về một tài khoản khác. |
| Tài khoản này hiện đã thuộc về một không gian làm việc khác | Vui lòng mở không gian làm việc đó thay vì thêm tài khoản hai lần. |
| Đã kết nối, nhưng danh sách trò chuyện trong **phần Nguồn** còn thiếu một nhóm riêng tư | Kiểm tra tư cách thành viên. Công cụ chọn lọc sẽ kiểm tra 1.000 cuộc đối thoại đầu tiên; quý vị có thể tăng giới hạn này trong **phần Thông số**. |
| Kết nối proxy không thành công | Kiểm tra chế độ định tuyến và chế độ IP. Chế độ MTProxy tự động sẽ thử một mục nhập khác đang hoạt động. Chế độ ẩn IP sẽ chờ; chế độ dự phòng được chọn rõ ràng có thể kết nối trực tiếp sau khoảng thời gian trễ đã cấu hình. Xem [các chế độ định tuyến](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/#ip-modes). |

Xem thêm: các vấn đề về [kết nối và bảo mật](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) liên quan đến máy chủ proxy và mã hóa, cũng như [cách thức thu thập dữ liệu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/) đối với những nội dung được ghi lại sau khi đăng nhập.
