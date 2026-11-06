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

You can sign in without creating a Telegram API application. When no pair is entered, imported or already saved in the workspace, TgWitness picks a pair from its built-in pool of 50 public API pairs (`tgwitness/api_pool.py`), preferring Telegram Desktop for a fresh login and retaining a saved pair first; remaining candidates are shuffled. If Telegram refuses a pair (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), the next one is tried, up to eight per sign-in; refused pairs are skipped until restart. The pair that signed in is saved with the account and reused for it. An **API ID** and **API hash** identify the application to Telegram; they do not authorize an account by themselves.

Missing connection fields use a deterministic device/OS pair from the bundled [opentele2 2.0.0 catalogs](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, and Web `2496`. Android's source-build ID `4` also uses the Android catalog, as identified in [Telegram Android's BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web defaults to A; an imported `K` app-version suffix or `macos` language pack selects K, and version `0.7.0` selects Webogram. Unknown application IDs keep Telethon's host defaults. Imported fields always win, including an older app version and an empty language pack. The catalog never changes the API ID/hash. Its version snapshot is reviewed explicitly, not fetched during login. A saved profile stays stable after updates.

`account.getAuthorizations` reports Telegram's saved authorization metadata; it is not an echo of each new `initConnection`. Compare it with the actual sent profile. Connecting an existing authorization does not validate its companion API hash: `initConnection` sends the API ID, while the hash is used by login requests.

After a new phone or QR authorization, TgWitness requests config, nearest DC, online status, languages (when the language pack is nonempty), app updates and terms-of-service updates, with 0.3–1.5 seconds between requests. Updating status briefly marks the account online. This sequence runs once at login completion, not on imports, reconnects or restarts. The authorization is saved first; a failed request stops the sequence without retrying or discarding the login. Results are recorded as `account.initialized`, with error names rather than response bodies. The sequence is not a guarantee against account restrictions.

For `tdesktop`, a missing `tz_offset` uses the server's local UTC offset, rounded to 900 seconds using the [opentele2 algorithm](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; license in `tgwitness/client_profiles.LICENSE`). It is refreshed on each connection so daylight-saving changes are reflected. An imported `tz_offset` takes precedence on every platform and is kept exactly, including zero. Other `initConnection.params` entries are retained. The HTTP sign-in form accepts the numeric timezone returned by file import; booleans, fractions and offsets outside the supported range are rejected.

Direct, SOCKS5 and HTTP CONNECT routes use Telethon's `ConnectionTcpObfuscated` (obfuscated abridged MTProto). HTTPS CONNECT retains TLS to the proxy and uses the same obfuscated transport inside the tunnel. MTProxy retains its required randomized intermediate transport and secret handling. Route switches apply the same choices. Obfuscation changes packet framing; it does not hide the account or its client metadata from Telegram or imply immunity to restrictions.

After connecting an authorized client, TgWitness checks config, nearest DC, the current authorization, the reviewed layer baseline, languages, app updates and terms-of-service updates. These diagnostics run once per client instance, before collection, and are shown under the connection details with their time. `account.connection_checked` records the result without session hashes, IPs, tokens or API hashes. They never accept terms or install updates. A request failure or FloodWait stops subsequent requests; a missing result stays unknown. Local checks can still report their results while network checks are skipped.

FloodWait diagnostics retain the failed TL method, any Takeout/range wrappers, the server-requested wait and the effective deadline in `telegram.backoff`. Connection details show the method and deadline while requests are paused. The diagnostic includes per-method client-call counters since that client was created; they count nested peer resolution separately, but do not count packets or Telethon's internal retry attempts. Current counters are also available as `collector.rpc_activity` in the status API. No request arguments, usernames, access hashes or exception text are included. The last diagnostic and full deadline survive restart. Earlier waits without a method record cannot be attributed retrospectively. See [export limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) for the source review and the distinction between discovery and history acquisition.

`official_app=True` or `False` is Telegram's current-authorization flag. Neither value establishes whether the account is restricted, trusted or under observation. The existing evidence-mode `account.devices` snapshots remain the history of all signed-in devices; connection diagnostics retain only the current device description.

Before connection, advisory checks compare the API platform, language pack, device/OS and app-version formats, mobile system locale, and Telethon's actual schema layer against the reviewed catalog baseline. Warnings appear in the server log and account status metadata; they never replace imported values or change the schema layer. A different layer is a compatibility review signal, not proof of a broken or restricted account. These checks and `official_app` do not certify that Telegram considers the account safe from restrictions. Disconnected account status uses the saved profile instead of generating another device description.

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

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Các tệp tin được chuyển đổi trực tiếp **trong bộ nhớ** trên máy chủ TgWitness của quý vị. Các tệp tải lên không được lưu trữ, các tệp ZIP không được giải nén ra đĩa và không có dịch vụ bên ngoài nào được liên hệ.
- Phiên ghi chép thu được sau đó sẽ được đối chiếu với Telegram. Nếu một tệp ghi nhận ID người dùng, thì ID đó phải trùng khớp với thông tin tài khoản mà Telegram cung cấp.
- Các tệp mô tả các tài khoản khác nhau hoặc thông tin đăng nhập API khác nhau sẽ bị từ chối thay vì chỉ chọn một tài khoản duy nhất.
- Trường **“Mật khẩu hoặc văn bản phiên làm việc”** chứa trường mật khẩu cục bộ TData, một ô để dán StringSession và **đọc tệp mà không cần đăng nhập** (điền biểu mẫu mà không cần liên hệ với Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

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
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData là thư mục `tdata` của ứng dụng Telegram Desktop (ứng dụng đa nền tảng từ desktop.telegram.org).

| Hệ thống | Vị trí mặc định `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (phiên bản Telegram di động: bên cạnh `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Để nhập dữ liệu:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
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
| `string_session` (`session_string`, `session_str`; legacy `session`) | Văn bản Telethon StringSession, không phải tên tệp |
| `auth_key` (`auth_key_hex`) + `dc_id` | Khóa xác thực (Auth Key) đầy đủ gồm 512 ký tự và DC 1–5 |
| `user_id` (`id`) | Tùy chọn; đã được đối chiếu với Telegram trước khi lưu thông tin ủy quyền |
| `device_model` (`device`) | Connection device description |
| `system_version` (`sdk`) | Connection OS version |
| `app_version` | Application version sent to Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Client language, system language and client language pack; an empty `lang_pack` is allowed |
| `tz_offset` | Optional UTC offset in seconds, sent in `initConnection.params`; integer or decimal integer string |

If both an alias and the main name are present, they must agree. Explicit Telethon session fields take priority over a generic `session` blob in another format. If both contain recognizable Telethon sessions, they must describe the same authorization. Without an explicit field, `session` must be a valid Telethon StringSession. Examples:

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
| Danh sách CSV/JSON của nhiều tài khoản | Nhập các tệp phiên được hỗ trợ qua **Tài khoản → Nhập tài khoản**, hoặc đăng nhập bằng số điện thoại/mã QR trong các không gian làm việc riêng biệt |
| Các phiên thử nghiệm (Test-DC) hoặc phiên bot | Vui lòng sử dụng tài khoản người dùng chính thức |

## Nhiều tài khoản

Hãy nhấn vào mã **+** bên cạnh trình chọn tài khoản, hoặc truy cập **Tài khoản → Cài đặt → Cài đặt kết nối → Không gian làm việc**, nhập tên nhãn và đăng nhập.

- Bất kỳ số lượng không gian làm việc nào, bao gồm cả không gian làm việc chính. Mỗi không gian làm việc đều có phiên làm việc, tuyến đường proxy , nguồn dữ liệu, chính sách ghi lại, sổ nhật ký, khóa ký, điểm kiểm tra và các tùy chọn xuất dữ liệu riêng biệt.
- Việc chuyển đổi không gian làm việc đang hiển thị sẽ không làm tạm dừng các không gian làm việc khác.
- Một sổ ghi chép luôn gắn liền với tài khoản đã tạo ra nó. Việc đăng nhập bằng một tài khoản khác yêu cầu phải có một không gian làm việc riêng, và một tài khoản không thể được gán cho hai không gian làm việc.
- Token bảng điều khiển chính quản lý tất cả các không gian làm việc. [Quyền truy cập được cấp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/) có thể giới hạn quyền của người khác đối với các tài khoản và cuộc trò chuyện đã chọn, kèm theo các quyền truy cập riêng biệt và giới hạn phiên làm việc.
- **Tài khoản** sẽ đổi tên một không gian làm việc và xóa một không gian làm việc đã thêm vào, cùng với phiên làm việc, nhật ký, các nguồn và khóa ký của không gian đó. Không gian làm việc chính không thể bị xóa khỏi bảng điều khiển.

### Nhập hàng loạt và nhóm tài khoản

Sử dụng **Accounts → Import accounts** để thêm nhiều tài khoản, ghép nối các tệp theo tên gốc và xem kết quả đăng nhập của từng tài khoản. Mỗi tài khoản sẽ có không gian làm việc riêng.

Một nhóm giúp tập hợp các tài khoản có liên quan lại với nhau mà không hợp nhất các phiên, khóa hoặc bằng chứng của chúng. **Mở nhóm** trên **Tài khoản** dẫn đến trang của nó tại `/groups/<id>`:

- **Tài khoản:** lộ trình kết nối, thông tin quan sát và tin nhắn cuối cùng của từng thành viên, kèm theo Bắt đầu**tất cả** và **Tạm dừng tất cả**.
- **Cần chú ý:** các tài khoản đã đăng xuất, không khả dụng hoặc gặp vấn đề về kết nối, nhập liệu, nguồn hoặc phương tiện; mỗi tên sẽ dẫn đến thẻ thông tin tương ứng.
- **Các cuộc trò chuyện trên nhiều tài khoản hiển thị:** các nguồn được chia sẻ, các tài khoản đang theo dõi chúng và các gián đoạn trong khoảng thời gian quan sát không gian làm việc có sẵn (tối đa bảy ngày). **Khi xuất với N tài khoản,** quá trình xuất kênh hoặc siêu nhóm sẽ được chia đều giữa các tài khoản này và tạo ra một tệp lưu trữ duy nhất.
- **Xuất nhóm:** một ZIP chứa bản xuất đã được ký của từng tài khoản dưới `accounts/` và `manifest.json` liệt kê các SHA-256 và dấu vân tay khóa của chúng, được ký bởi không gian làm việc chính trong `manifest.signature.json`. Xác minh từng bản lưu trữ tài khoản riêng lẻ bằng `python -m tgwitness.verify` và dấu vân tay đáng tin cậy của tài khoản đó.

Các thành viên chia sẻ cài đặt chung của nhóm; mỗi tài khoản có thể giữ nguyên các giá trị riêng của mình. Xem [phần cài đặt chung](https://phishdestroy.github.io/TgWitness/vi/docs/reference/settings/#account-groups), [hướng dẫn nhập dữ liệu và quản lý nhóm](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) cùng với [bảng điều khiển nhóm MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Đăng xuất

**Tài khoản → Đăng xuất khỏi Telegram** (với chế độ quan sát tạm dừng) sẽ yêu cầu Telegram kết thúc phiên làm việc, do đó phiên này cũng sẽ biến mất khỏi mục **Cài đặt → Thiết bị** của tài khoản, đồng thời xóa phiên làm việc khỏi kho lưu trữ không gian làm việc. Nhật ký, các nguồn, cài đặt và khóa ký vẫn được giữ lại, và nhật ký sẽ ghi lại thao tác đăng xuất này. Không gian làm việc vẫn thuộc về tài khoản đó: chỉ có tài khoản đó mới có thể kết nối lại với nó. Nếu Telegram không phản hồi, phiên làm việc vẫn sẽ bị xóa tại đây và bảng điều khiển sẽ hiển thị thông báo tương ứng; quý vị hãy kết thúc phiên làm việc trong Telegram tại **Cài đặt → Thiết bị**.

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
| Kết nối proxy không thành công | Kiểm tra chế độ định tuyến và IP. Tự động MTProxy sẽ thử một mục nhập khác đang hoạt động. Chế độ ẩn địa chỉ sẽ chờ; chế độ Trực tiếp (Direct) là phương án cuối cùng, có thể kết nối trực tiếp sau thời gian trễ đã cấu hình. Xem [các chế độ định tuyến](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/#ip-modes). |

Xem thêm: các vấn đề về [kết nối và bảo mật](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) liên quan đến máy chủ proxy và mã hóa, cũng như [cách thức thu thập dữ liệu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/) đối với những nội dung được ghi lại sau khi đăng nhập.
