# Cài đặt, xác minh và cập nhật

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/installation/

Cài đặt chỉ với một lệnh, kiểm tra chữ ký và mã băm, cập nhật và gỡ bỏ cài đặt.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Dự án](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Hướng dẫn nhanh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/) · [Triển khai](https://phishdestroy.github.io/TgWitness/vi/docs/reference/deployment/)

**On this page**

- [Install with one command](https://phishdestroy.github.io/TgWitness/vi/docs/reference/installation/#install-with-one-command)
- [Where everything runs](https://phishdestroy.github.io/TgWitness/vi/docs/reference/installation/#where-everything-runs)
- [Full-text search settings](https://phishdestroy.github.io/TgWitness/vi/docs/reference/installation/#full-text-search-settings)
- [Command-line access](https://phishdestroy.github.io/TgWitness/vi/docs/reference/installation/#command-line-access)
- [Verify before running](https://phishdestroy.github.io/TgWitness/vi/docs/reference/installation/#verify-before-running)
- [Update an existing installation](https://phishdestroy.github.io/TgWitness/vi/docs/reference/installation/#update-an-existing-installation)
- [Everyday commands on Ubuntu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/installation/#everyday-commands-on-ubuntu)
- [Remove TgWitness](https://phishdestroy.github.io/TgWitness/vi/docs/reference/installation/#remove-tgwitness)

## Cài đặt chỉ với một lệnh

Trình cài đặt có hướng dẫn đi kèm bao gồm một môi trường chạy Python riêng tư. Sử dụng cùng một địa chỉ cho các lần cài đặt sau này: mỗi bản phát hành sẽ cập nhật đồng thời trình cài đặt, các giá trị băm, chữ ký và thông tin bản dựng.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Trên máy chủ Ubuntu, hãy chạy với quyền root để cài đặt dịch vụ chạy nền. Trên máy tính để bàn, hãy chạy với tư cách người dùng thông thường.

**Windows (PowerShell hoặc Command Prompt):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Không cần quyền quản trị viên trên Windows. Quy trình con PowerShell sẽ giữ cho cửa sổ terminal của bạn mở với kết quả hiển thị. Python và các phụ thuộc được giữ lại trong thư mục cài đặt.

Trên Ubuntu, hãy chọn **"Máy tính này**", **"Liên kết HTTPS tạm thời**" hoặc **"Miền riêng**". Trình cài đặt sẽ hiển thị địa chỉ bảng điều khiển và khóa truy cập. Đối với liên kết tạm thời, hãy mở địa chỉ HTTPS đó trong trình duyệt của bạn và nhập khóa. Với quyền truy cập cục bộ trên máy chủ từ xa, hãy sử dụng chuyển tiếp SSH từ máy tính của bạn (`ssh -L 8787:127.0.0.1:8787 user@server`) và mở `http://127.0.0.1:8787`. Trên macOS và Windows, bảng điều khiển cục bộ sẽ mở trong trình duyệt của bạn; hãy giữ cho cửa sổ terminal của nó tiếp tục chạy.

Đăng nhập vào Telegram trong bảng điều khiển và chọn những nội dung cần thu thập. Chỉ cài đặt thôi thì chưa đủ để bắt đầu thu thập dữ liệu từ Telegram.

## Nơi mọi thứ hoạt động

`get.destroy.tools` là một **Cloudflare Worker phục vụ các tệp tải xuống tĩnh**. Nó không có bảng TgWitness, phiên Telegram hoặc cơ sở dữ liệu bằng chứng người dùng. Nó không được định tuyến đến một máy chủ ảo (VPS) của dự án. Ứng dụng chạy trên máy tính nơi bạn thực thi lệnh.

| Cài đặt | Chương trình | Dữ liệu |
| --- | --- | --- |
| Ubuntu với quyền root | `/opt/tgwitness` | Dịch vụ hệ thống: `/var/lib/tgwitness-<installation ID>`; sử dụng `tgwitness paths` để biết đường dẫn chính xác. |
| Người dùng Linux / macOS | `~/.local/share/tgwitness` | `data/live` trong quá trình cài đặt đó. |
| Người dùng Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` trong quá trình cài đặt đó. |

Chọn `TGWITNESS_INSTALL_DIR` để chọn một thư mục khác. Các phiên bản đã cài đặt và dữ liệu được tách biệt. Trình cài đặt không tải lên tài khoản, tin nhắn hoặc khóa của bạn lên trang web tải xuống. Chọn đường hầm Cloudflare sẽ chuyển lưu lượng truy cập bảng điều khiển qua Cloudflare; sử dụng tên miền riêng của bạn sẽ trỏ đến máy chủ của chính bạn.

Mỗi bản cài đặt đều bao gồm **các tệp START-HERE.html** và **START-HERE.txt**, với các đường dẫn cục bộ, lệnh và liên kết đến kho lưu trữ. Chạy `tgwitness guide` để mở hướng dẫn. Trên Windows, hãy sử dụng `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` trong PowerShell.

## Cài đặt tìm kiếm toàn văn

[Tính năng tìm kiếm toàn văn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/search/) (bản xem trước) không cần thiết lập. Chỉ mục của nó được xây dựng ở chế độ nền sau khi cập nhật.

| Biến hoặc lệnh | Hiệu quả |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Mặc định: chỉ mục được lưu trữ trong `search/fulltext.sqlite3` của mỗi không gian làm việc |
| `TGWITNESS_FULLTEXT=memory` | Không có tệp chỉ mục; chỉ mục được xây dựng lại mỗi khi khởi động |
| `TGWITNESS_FULLTEXT=off` | Không có chỉ mục; chỉ tìm kiếm theo văn bản chính xác |
| `tgwitness index status` | Trạng thái chỉ mục của mỗi không gian làm việc |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Xây dựng lại mọi chỉ mục từ nhật ký được ký điện tử |

Lựa chọn của quản trị viên trong **Nhật ký → Bộ lọc → Chỉ mục tìm kiếm** sẽ ghi đè lên biến cho không gian làm việc đó. Các lệnh sẽ tìm thư mục dữ liệu của bản cài đặt chạy chúng; ở các vị trí khác, hãy thêm `--data-dir` với đường dẫn từ `tgwitness paths`. Để có từ điển tiếng Ukraina đầy đủ (dữ liệu GPL-3.0), hãy cài đặt `pymorphy3-dicts-uk` trong môi trường Python của bản cài đặt.

## Truy cập qua dòng lệnh

[Dòng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/cli/) [lệnh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/cli/) (bản xem trước) đọc tệp lưu trữ để tìm các tập lệnh và tác nhân.

| Biến | Hiệu quả |
| --- | --- |
| `TGWITNESS_URL` | Địa chỉ bảng điều khiển cho `tgwitness search`, `context`, `messages`, `stats` và `export`; mặc định `http://127.0.0.1:8787` khi đã thiết lập mã thông báo |
| `TGWITNESS_MCP_TOKEN` | Lưu trữ mã thông báo kết nối từ **mục Tích hợp → MCP**, được chia sẻ với các khách hàng MCP; `--token-file` thay vào đó, đọc nó từ một tệp |
| `TGWITNESS_DATA` | Thư mục dữ liệu được đọc trực tiếp khi không `--data-dir`, URL hoặc mã thông báo nào được cung cấp |

## Kiểm tra trước khi chạy

Lệnh một dòng này tin cậy HTTPS cho tập lệnh ban đầu của nó. Tập lệnh đó kiểm tra SHA-256 và chữ ký RSA của dự án trên ứng dụng cũng như các ràng buộc trước khi cài đặt. Bạn cũng có thể tải xuống và xác minh tập lệnh ban đầu trước.

Khóa công khai là [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). SHA-256 của nó là:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Hãy lưu giữ dấu vân tay này từ một phiên bản kho lưu trữ mà bạn tin cậy. Tổng kiểm tra từ cùng một máy chủ tải xuống sẽ phát hiện sự không khớp; khóa công khai được tin cậy độc lập chính là yếu tố xác thực chữ ký bản phát hành.

Hãy sử dụng một thư mục mới, trống để chứa các tệp tải xuống xác minh dưới đây.

**Linux / macOS — chạy trong một thư mục tải xuống mới và trống** (yêu cầu curl và OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

Quá trình `&&` chuỗi sẽ dừng lại trước khi thực thi nếu quá trình tải xuống, kiểm tra dấu vân tay khóa hoặc kiểm tra chữ ký không thành công. Nếu có bản phát hành mới trong khoảng thời gian từ khi tải xuống tập lệnh đến khi kiểm tra chữ ký, hãy tải lại cả hai. Các trình cài đặt cũ vẫn giữ nguyên URL gói không thể thay đổi của chúng.

**Windows — hãy kiểm tra thẻ SHA-256 trước khi chạy:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

So sánh giá trị băm với `install.ps1` dòng này. Để kiểm tra chữ ký độc lập, hãy sử dụng OpenSSL (ví dụ: từ Git Bash) và dấu vân tay khóa công khai tương tự như trên:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Quá trình cài đặt trên Windows tự động xác minh chữ ký gói bằng .NET và không cần OpenSSL. Đây là các chữ ký RSA-3072 / SHA-256 độc lập, không phải Authenticode. Bản [kê khai](https://get.destroy.tools/manifest.json) ghi lại phiên bản phần mềm, cam kết Git chính xác, ID bản phát hành bất biến và SHA-256 của từng thành phần. Trang này liên kết đến nguồn tương ứng. Bản kê khai và danh sách tổng kiểm tra cũng có các chữ ký độc lập (`manifest.json.sig` và `SHA256SUMS.txt.sig`).

## Cập nhật bản cài đặt hiện có

**Một bản phát hành mới sẽ cập nhật trang tải xuống; các chương trình đã cài đặt sẽ được cập nhật khi bạn chạy trình cài đặt lại.** Không có trình cập nhật tự động hoặc tính năng khởi động lại tự động cho bộ sưu tập đang chạy. Kênh trình cài đặt hiện tại là **bản xem trước**; nó dựa trên các bản dựng đã được phát hành và kiểm tra từ `main`, trong đó commit có thể mới hơn so với bản phát hành GitHub được đánh số gần nhất. Phiên bản của trang này xuất phát từ `pyproject.toml`; cam kết và ID bản dựng của nó giúp phân biệt các bản cập nhật trong cùng một phiên bản xem trước.

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

Sử dụng cùng thư mục cài đặt và tài khoản người dùng hệ điều hành như trước đây. Sao lưu toàn bộ thư mục dữ liệu khi quá trình thu thập dữ liệu đã dừng; `tgwitness paths` xác định nó. Một tệp xuất đã được ký không phải là bản sao lưu cài đặt đầy đủ.

**Cài đặt Ubuntu với quyền root tại `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Sau khi cài đặt thành công:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Đối với người dùng Linux/macOS, hãy sử dụng bản gốc `TGWITNESS_INSTALL_DIR` hoặc cài đặt mặc định và chạy lại lệnh cài đặt đầu tiên. Đóng bảng điều khiển đang chạy ở chế độ nền trước khi cập nhật và khởi động lại nó sau đó. Đối với dịch vụ đã được cấu hình trên Linux, hãy chạy lệnh `tgwitness restart` lệnh đó.

**Windows:** đóng bảng điều khiển đang chạy, chạy lại lệnh cài đặt Windows, sau đó mở `bin\tgwitness.cmd` trong cùng một bản cài đặt. Trình cài đặt sẽ giữ lại dữ liệu, phiên làm việc, cài đặt truy cập và khóa ký. Trình khởi chạy chỉ được chuyển đổi sau khi môi trường mới vượt qua các bước kiểm tra; nếu cài đặt thất bại, trình khởi chạy trước đó sẽ vẫn được giữ nguyên. Hãy giữ bản sao lưu trước khi nâng cấp để đề phòng các thay đổi về định dạng lưu trữ.

## Các lệnh thường dùng trên Ubuntu

| Lệnh | Kết quả |
| --- | --- |
| `tgwitness open` | URL bảng điều khiển hiện tại và khóa truy cập. |
| `tgwitness paths` | Đường dẫn chính xác đến chương trình, dữ liệu và hướng dẫn. |
| `tgwitness guide --print` | Hướng dẫn sử dụng ngoại tuyến. |
| `tgwitness status` / `tgwitness logs` | Tình trạng sẵn sàng / nhật ký dịch vụ. |
| `tgwitness stop` / `tgwitness start` | Dừng / tiếp tục dịch vụ; giữ lại dữ liệu. |
| `tgwitness token rotate` | Thay thế khóa quản trị viên và kết thúc các phiên trình duyệt. |
| `tgwitness tunnel off` | Vô hiệu hóa đường hầm nhanh công khai; giữ lại bảng điều khiển cục bộ. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Tạo liên kết đường hầm nhanh / thay thế địa chỉ của nó. |

Xem [phần Quyền truy cập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/) để biết thông tin về mã thông báo đồng nghiệp, phiên làm việc và hạn chế IP, cũng như [phần Xuất bản trình cài đặt](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) để tìm hiểu quy trình phát hành từ GitHub sang Cloudflare.

## Xóa TgWitness

Không có trình gỡ cài đặt: bạn chỉ cần tắt bảng điều khiển và xóa các thư mục của nó. Việc xóa thư mục dữ liệu sẽ xóa vĩnh viễn các nhật ký, khóa ký, phiên Telegram và các tệp đã lưu. Trước khi thực hiện điều đó:

1. Xuất những gì bạn cần (**Xuất → Tải xuống tệp đã ký ZIP**) và lưu giữ dấu vân tay khóa ký cùng các điểm kiểm tra bên ngoài máy này. Để giữ lại chính không gian làm việc, hãy sao chép toàn bộ thư mục dữ liệu khi quá trình thu thập đã dừng lại.
2. Xóa các máy chủ được tạo trong mục **Extras → Server 24/7** từ **phần "Your servers"** hoặc bằng `python -m tgwitness.cloud destroy`; nhà cung cấp sẽ tính phí cho các máy chủ này cho đến khi chúng được xóa.
3. Kết thúc phiên làm việc của từng tài khoản trên Telegram tại **mục Cài đặt → Thiết bị**. Việc xóa các tệp này sẽ không đăng xuất phiên làm việc đó trên phía Telegram.

**Cài đặt với quyền root trên Ubuntu.** Lưu ý thư mục dữ liệu, dừng dịch vụ, sau đó xóa dịch vụ, các thư mục và lối tắt:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Cài đặt cho người dùng Linux hoặc macOS.** Đóng bảng điều khiển. Dịch vụ người dùng Linux đã được cấu hình sẽ bị dừng bằng `systemctl --user disable --now tgwitness-<ID>`; đơn vị của nó nằm trong `~/.config/systemd/user/`. Sau đó xóa `~/.local/share/tgwitness` (hoặc của bạn `TGWITNESS_INSTALL_DIR`) và `~/.local/bin/tgwitness` lối tắt.

**Windows.** Đóng bảng điều khiển và xóa `%LOCALAPPDATA%\TgWitness` (hoặc `TGWITNESS_INSTALL_DIR`). Trình cài đặt không thêm bất kỳ dịch vụ, tác vụ được lên lịch hoặc lối tắt nào.
