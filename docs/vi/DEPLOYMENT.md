[TgWitness](../../README.md) / [Tài liệu hướng dẫn](../README.md) / [Thư mục](README.md)

![Triển khai và khôi phục](../assets/presentation/chapter-operate.svg)

[English](../DEPLOYMENT.md) · [Русский](../ru/DEPLOYMENT.md) · [Українська](../uk/DEPLOYMENT.md) · [Español](../es/DEPLOYMENT.md) · [Português (Brasil)](../pt/DEPLOYMENT.md) · [Türkçe](../tr/DEPLOYMENT.md) · [العربية](../ar/DEPLOYMENT.md) · [فارسی](../fa/DEPLOYMENT.md) · [اردو](../ur/DEPLOYMENT.md) · [हिन्दी](../hi/DEPLOYMENT.md) · [Bahasa Indonesia](../id/DEPLOYMENT.md) · **Tiếng Việt** · [简体中文](../zh/DEPLOYMENT.md)

# Triển khai và vận hành

## Chọn cách cài đặt

Đối với gói di động, hãy giải nén tệp `TgWitness-<version>-windows-amd64-portable.zip` từ
GitHub Releases. Đối với các phương pháp khác, hãy tải xuống và giải nén tệp ZIP chứa mã nguồn hoặc sao chép
kho lưu trữ, sau đó chạy lệnh sau từ thư mục dự án:

| Cài đặt | Bắt đầu | Chạy ngầm? |
| --- | --- | --- |
| Gói phần mềm di động cho Windows | `TgWitness.cmd` | Không; hãy để cửa sổ mở. |
| Windows gốc | `Start.cmd` | Không; hãy sử dụng tác vụ đăng nhập tùy chọn để chạy ở chế độ nền. |
| Dành riêng cho Linux/macOS | `sh start.sh` | Không; hãy sử dụng systemd/launchd để chạy nền. |
| Docker trên bất kỳ máy chủ nào được hỗ trợ | `docker compose up -d --build --wait` | Đúng vậy, miễn là daemon Docker vẫn đang chạy. |
| Trình hỗ trợ Docker trên Windows | `scripts\Docker.cmd` | Đúng vậy; trình hỗ trợ sẽ theo dõi tình trạng hoạt động của máy chủ web. |
| Công cụ hỗ trợ Docker trên Linux/macOS | `sh scripts/docker-start.sh` | Đúng vậy; trình hỗ trợ sẽ theo dõi tình trạng hoạt động của máy chủ web. |

Đối với một máy chủ đám mây mà bên thứ ba có thể kiểm tra — được tạo thông qua
API của nhà cung cấp, không sử dụng SSH, chỉ có thể truy cập thông qua Cloudflare Tunnel — hãy tham khảo
[cài đặt có độ tin cậy cao](../HIGH-ASSURANCE.md).

Ứng dụng khởi động gốc sẽ tạo một hình ảnh riêng tư `.venv` và cài đặt các phụ thuộc đã được ghim.
Docker sẽ biên dịch chúng bên trong hình ảnh, mà không cần đến Python trên máy chủ. Lần
cài đặt đầu tiên cần có kết nối Internet. Khi không tìm thấy Python 3.11 trở lên, `Start.cmd` sẽ hỏi ý kiến người dùng trước khi
cài đặt Python 3.12 cho người dùng Windows hiện tại (sử dụng winget, hoặc trình cài đặt từ python.org
sau khi kiểm tra chữ ký của Python Software Foundation); quá trình này không bao giờ yêu cầu
quyền quản trị viên. Docker và các dịch vụ hệ điều hành vẫn là các điều kiện tiên quyết.

Các bản cài đặt gốc và di động sử dụng `data/live` bên trong thư mục của chúng. Docker sử dụng khối lượng có tên `tgwitness-data`
tại `/data`. Đây là các bản cài đặt riêng biệt cho đến khi bạn chủ động di chuyển
toàn bộ thư mục dữ liệu. Đừng mong đợi một container Docker mới sẽ tự động phát hiện
các tài khoản gốc.

## Yêu cầu cài đặt

Việc cài đặt bản gốc yêu cầu Python 3.11 trở lên cùng với `venv` và `ensurepip`, kết nối
Internet để cài đặt các phụ thuộc ban đầu, và một thư mục dự án có quyền ghi cho
`.venv`. Bảng điều khiển đi kèm không cần Node.js hay quá trình biên dịch frontend. Hãy chạy trình khởi chạy từ
tài khoản hệ điều hành thông thường của bạn; TgWitness không yêu cầu quyền quản trị viên/root.

- **Windows:** `Start.cmd` sẽ kiểm tra `py -3`, sau đó là `python`, tiếp theo là các thư mục cài đặt mặc định theo người dùng và
  thư mục Program Files, và yêu cầu phiên bản 3.11 trở lên. Nếu không có cách nào thành công, nó
  sẽ đề xuất cài đặt tự động theo người dùng như đã mô tả ở trên. `py -3 start.py` cũng hoạt động.
  Gói di động hoàn toàn không cần Python.
- **Linux:** `start.sh` sẽ kiểm tra `python3.13`, `python3.12`, `python3.11`, `python3` và
  `python`, đồng thời hiển thị lệnh cài đặt cho apt, dnf, pacman, zypper, apk hoặc Homebrew
  khi không có tùy chọn nào đáp ứng yêu cầu. Các bản cài đặt trên Debian/Ubuntu có thể yêu cầu gói
  `python3-venv` tương ứng với trình thông dịch đã chọn. Phiên bản Python mặc định cũ hơn
  của hệ điều hành phải được thay thế hoặc bổ sung bằng Python 3.11 trở lên.
- **macOS:** cài đặt phiên bản Python 3.11 trở lên mới nhất; không nên giả định rằng trình thông dịch
  do hệ điều hành cung cấp đáp ứng yêu cầu. Sử dụng `python3 start.py` từ thư mục dự án.
- **Docker:** sử dụng Docker Engine/Desktop với Compose v2.20 trở lên. Docker Desktop
  phải sử dụng các container Linux trên Windows. Container sẽ tự cài đặt các
  tùy thuộc Python của riêng mình; máy chủ không cần cài đặt Python riêng biệt.

## Máy tính cục bộ

Sử dụng `Start.cmd` trên Windows hoặc `sh start.sh` trên Linux/macOS. `scripts\Setup.cmd` hoặc
`sh start.sh --setup-only` sẽ chuẩn bị
môi trường. Trình khởi chạy sẽ cài đặt các thành phần phụ thuộc khi sử dụng lần đầu; các lần khởi chạy
sau đó sẽ tái sử dụng môi trường này. Cần có kết nối Internet để thiết lập và thu thập dữ liệu từ Telegram,
nhưng việc duyệt các bản ghi hiện có và tạo tệp xuất vẫn hoạt động ở chế độ ngoại tuyến.

Chạy lệnh `python start.py --check` sau khi cài đặt để kiểm tra các phụ thuộc cục bộ, Ed25519,
bộ nhớ, cấu hình khóa và địa chỉ lắng nghe mà không cần khởi động bộ thu thập.
Sử dụng `--json` để có kết quả đầu ra có cấu trúc. Truyền các tham số `--data-dir`, `--host` và
`--port` theo ý định. Quá trình kiểm tra này không cài đặt gói phần mềm, không tạo nhật ký hoặc kết nối với Telegram;
đây không phải là quá trình xác nhận tính toàn vẹn hoặc phạm vi bao phủ. Quá trình khởi động sẽ xác minh riêng biệt
các nhật ký hiện có. `python start.py --help` cũng tránh việc cài đặt.

Sau khi chạy start.py, hãy thực thi các lệnh phụ trợ bằng `.venv\Scripts\python.exe` trên
Windows hoặc `.venv/bin/python` trên Linux/macOS, hoặc kích hoạt môi trường đó trước.
Các ví dụ `python -m ...` dưới đây giả định rằng môi trường đã được kích hoạt.

~~~sh
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
~~~

Biến môi trường: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN.
TGWITNESS_VAULT_KEY_FILE chọn chế độ khóa bên ngoài cho một cài đặt mới; xem [Khóa chính bên ngoài](../SECURITY-MODEL.md#external-master-key).
TGWITNESS_TOKEN, nếu được cung cấp, phải chứa ít nhất 24 ký tự; hãy sử dụng một giá trị ngẫu nhiên
theo tiêu chuẩn mật mã. Nếu không có giá trị này, ứng dụng sẽ tạo ra một mã thông báo ngẫu nhiên 256-bit trong tệp panel-token.txt.
Việc ghi đè môi trường sẽ không ghi đè lại tệp đó. Khởi động lại để luân chuyển thông tin xác thực.

Chỉ có đúng một tiến trình được phép sở hữu một thư mục dữ liệu. Cơ chế khóa tệp đa nền tảng của hệ điều hành ngăn chặn
việc ghi đồng thời vô tình. Sử dụng một worker Uvicorn. Bảng điều khiển có thể quản lý bất kỳ số lượng
không gian làm việc nào, với các thư mục không gian làm việc bổ sung nằm trong thư mục profiles/<id>/.
Đối với các phiên bản dịch vụ riêng biệt, hãy sử dụng các thư mục và cổng riêng biệt. Các tệp WAL của SQLite phải được lưu trữ trên bộ nhớ bền vững cục bộ,
chứ không phải trên hệ thống tệp mạng. Không chia sẻ một khối lượng lưu trữ giữa các bản sao.

## Gói portable cho Windows

Mỗi bản phát hành trên GitHub đều chứa `TgWitness-<version>-windows-amd64-portable.zip` và
`.sha256`. Nó bao gồm môi trường chạy Python 3.12 chính thức có thể nhúng từ python.org
(tổng kiểm tra được cố định trong `tools/build_portable.py`), TgWitness cùng các phụ thuộc được cố định của nó,
và ba trình khởi chạy:

| Tệp | Mục đích |
| --- | --- |
| `TgWitness.cmd` | Khởi chạy bảng điều khiển; các tùy chọn bổ sung sẽ được truyền vào, ví dụ: `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Khởi chạy bản demo tổng hợp tại `data\demo` |
| `TgWitness-Check.cmd` | Chạy kiểm tra mức độ sẵn sàng mà không khởi động |

Từ điển hình thái học tiếng Nga đã được ghim và các cấu hình màu PDF được gói chung lại để
sử dụng ngoại tuyến. Quá trình đóng gói chỉ cho phép các đường dẫn tệp đã biết nằm trong các thư mục phụ thuộc
`data`; các tệp không mong muốn trong các thư mục đó sẽ khiến quá trình xây dựng thất bại.

Giải nén toàn bộ tệp lưu trữ vào một thư mục có thể ghi được, chẳng hạn như `Documents\TgWitness`; không chạy
chương trình từ bên trong tệp ZIP hoặc từ thư mục Program Files. Môi trường chạy sử dụng đường dẫn mô-đun cách ly,
nên các bản cài đặt Python khác và `PYTHONPATH` sẽ không ảnh hưởng đến nó. Dữ liệu được lưu trữ trong
thư mục `data` của gói phần mềm. Để cập nhật, hãy dừng TgWitness, giải nén phiên bản mới vào một
thư mục mới và sao chép thư mục `data` sang đó.

Tự biên dịch trên hệ điều hành Windows 64-bit bằng Python 3.12:

~~~sh
python tools/build_portable.py
~~~

## Container

```sh
docker compose up -d --build --wait
```

Điều này sẽ tạo ra một khối lượng lưu trữ vĩnh viễn có tên cho /data.
Cổng web được ánh xạ đến 127.0.0.1:8787. Quy trình chạy với UID 10001 cùng các
quyền hạn bị giới hạn, hệ thống tệp gốc chỉ đọc, và các thư mục /data và /tmp có thể ghi.
`--wait` kiểm tra tình trạng hoạt động của máy chủ web trước khi trả về kết quả; quá trình xác thực và
gửi tin nhắn Telegram sẽ hiển thị trên bảng điều khiển. Các hàm trợ giúp được cung cấp sử dụng thời gian chờ sẵn sàng là 180 giây
sau khi xây dựng. Việc tải xuống các phụ thuộc ban đầu có thể mất nhiều thời gian hơn mức đó.

Cả hai tệp Compose cơ sở đều sử dụng tên dự án `tgwitness`, do đó việc giải nén một bản phát hành mới
vào một thư mục khác sẽ không tự động chọn một khối dữ liệu mới. Chỉ nên duy trì một
bản triển khai đang hoạt động cho dự án đó. Đối với các cài đặt độc lập, hãy sử dụng một
`docker compose -p NAME ...` duy nhất và cổng máy chủ khác, đồng thời giữ nguyên cả hai khi cập nhật.
Đối với một bản triển khai cũ hơn sử dụng tên dự án khác, hãy tiếp tục sử dụng tên ban đầu
của nó với `-p`; `docker compose ls` liệt kê các dự án hiện có.

Sao chép `deploy/env.example` vào `.env` và thay đổi `TGWITNESS_PORT` để sử dụng một cổng loopback
khác. Ví dụ: `TGWITNESS_PORT=8788` hiển thị bảng điều khiển tại
`http://127.0.0.1:8788`; container vẫn lắng nghe trên cổng 8787. `.env` bị Git bỏ qua.

Lấy mã thông báo ban đầu:

~~~sh
docker compose exec tgwitness cat /data/panel-token.txt
~~~

Các lệnh hữu ích:

```sh
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` sẽ khởi động lại trình thu thập sau khi xảy ra sự cố hoặc khi daemon Docker
được khởi động lại. Trên máy chủ Linux, hãy kích hoạt Docker khi khởi động bằng trình quản lý dịch vụ
của bản phân phối hệ điều hành, thường là `sudo systemctl enable --now docker`. Trên Windows/macOS, hãy kích hoạt
cài đặt “khởi động khi đăng nhập” của Docker Desktop. Việc đăng xuất khỏi Desktop, chuyển sang chế độ ngủ hoặc khi daemon
có thể làm gián đoạn quá trình thu thập dữ liệu. Một container bị dừng rõ ràng sẽ vẫn
ở trạng thái dừng cho đến khi bạn khởi động lại nó.

Trong cấu hình ví dụ, dung lượng của phân vùng /tmp bị giới hạn ở mức 512 MiB. Quá trình xuất dữ liệu
sẽ sử dụng tệp `temporary-exports/` của từng không gian làm việc trên phân vùng /data bền vững thay thế. Cần dành dung lượng
tại đó cho các tác vụ xuất dữ liệu đồng thời, sự gia tăng của nhật ký/WAL, tệp phương tiện và bản sao lưu.
Trình khởi chạy sử dụng tệp deploy/constraints.txt để cố định các phiên bản phụ thuộc thời gian chạy đáp ứng yêu cầu.
Các máy chủ Docker và máy chủ có độ tin cậy cao được cài đặt từ deploy/requirements.lock và
deploy/build.lock bằng lệnh pip --require-hashes: mỗi tệp gói phải khớp với mã SHA-256
được ghi lại trong commit, do đó tệp bị thay thế trên PyPI hoặc máy chủ gương sẽ bị từ chối. Các gói
chỉ cung cấp mã nguồn (jieba, pyaes) được xây dựng bằng setuptools được cố định trong deploy/build.lock
(`--no-build-isolation`) bởi trình khởi chạy, trình xây dựng di động trên Windows và tệp Dockerfile,
do đó pip không giải quyết một môi trường xây dựng riêng biệt, không được cố định. Hình ảnh cơ sở Python
và các gói hệ điều hành vẫn yêu cầu quá trình kiểm định phiên bản độc lập.

Không nên sử dụng lệnh `docker compose down -v` trừ khi bạn có ý định xóa nhật ký và các khóa.
Báo cáo tình trạng container phản ánh tình trạng sẵn sàng của máy chủ web, chứ không phải việc thu thập dữ liệu Telegram thành công.
Kiểm tra trạng thái bộ thu thập, tín hiệu kiểm tra hoạt động, lỗi và các sự kiện phạm vi phủ sóng trên bảng điều khiển.

### Profile nhân chứng độc lập

Dịch vụ tùy chọn `witness` chạy một [nhân chứng độc lập](../WITNESS.md) trong
container riêng của nó, với khóa và nhật ký riêng trong khối lượng `witness-data` và chỉ có một
mã thông báo nhân chứng chỉ đọc dành cho bộ thu thập. Tạo mã thông báo trong bảng điều khiển tại mục **Công cụ khác → Tiện ích → Nhân chứng độc lập**, thêm mã thông báo này
cùng với mã thông báo bot và kênh vào `.env`, sau đó khởi động cấu hình:

```sh
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Dịch vụ này kết nối với bộ thu thập dữ liệu trong mạng Compose tại `http://tgwitness:8787`
(`TGWITNESS_WITNESS_COLLECTOR`
sẽ ghi đè lên nó, ví dụ như `/profiles/<workspace ID>`
dành cho
một không gian làm việc khác). Đối với tệp chứng thực trên một máy chủ riêng biệt, do người khác quản lý, hãy sử dụng
`deploy/compose/compose.witness.yaml`
tại đó và đặt `TGWITNESS_WITNESS_COLLECTOR`
thành địa chỉ HTTPS
của bộ thu thập dữ liệu; tệp đó chỉ chứa tệp chứng thực.

## Cài đặt image đã phát hành

Sao chép `deploy/env.example` vào `.env`. Đặt `TGWITNESS_IMAGE` thành phiên bản đã xuất bản, bằng cách sử dụng
đường dẫn kho lưu trữ **viết thường**, ví dụ:

```dotenv
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:1.0.2
TGWITNESS_PORT=8787
```

Hãy chạy tệp này một cách độc lập, thay vì sử dụng thẻ `compose.yaml`:

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Không cần mã nguồn, Python hay trình biên dịch trên máy chủ. Quy trình phát hành
nhắm đến các container Linux AMD64 và ARM64, bao gồm cả máy ảo Linux của Docker Desktop.
Sử dụng thẻ phiên bản hoặc `ghcr.io/owner/repository@sha256:...` từ bản tóm tắt quy trình làm việc.
Không có cấu hình cho thẻ `latest` di chuyển hoặc nâng cấp ứng dụng tự động. Các
biến thể hình ảnh và mã nguồn sử dụng cùng một khối lượng dữ liệu khi tên dự án của chúng trùng khớp.

## HTTPS tự động trên máy chủ

Sử dụng một máy chủ chạy Docker, một tên miền do bạn quản lý và bộ nhớ cục bộ bền vững.
Định hướng các bản ghi A/AAAA của tên miền đến máy chủ; chỉ công bố bản ghi AAAA nếu địa chỉ IPv6 truy cập
được máy chủ. Cho phép lưu lượng TCP 80 và 443 đến và lưu lượng DNS/HTTPS đi để cấp chứng chỉ.
Các dịch vụ khác không được sử dụng các cổng này.

Sao chép `deploy/env.example` vào `.env` và đặt tên máy chủ, không kèm theo lược đồ hoặc đường dẫn:

```dotenv
TGWITNESS_DOMAIN=watch.your-domain.org
```

Bắt đầu quá trình biên dịch mã nguồn với lớp phủ HTTPS:

```sh
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

Đối với hình ảnh đã được xuất bản, hãy sử dụng thẻ `deploy/compose/compose.image.yaml` làm tệp đầu tiên thay thế. Giữ lại
cả hai tham số `-f` để sử dụng cho các lệnh trạng thái, ghi nhật ký, cập nhật và dừng sau này.

Caddy thực hiện việc cấp và gia hạn chứng chỉ, chuyển hướng HTTP sang HTTPS, đồng thời chuyển tiếp
các yêu cầu đến bộ thu thập trên mạng Compose riêng. Trạng thái chứng chỉ có
khối lượng lưu trữ bền vững riêng. Cổng máy chủ trực tiếp của bộ thu thập vẫn chỉ hoạt động ở chế độ loopback.
Cấu hình Caddy được cung cấp không kích hoạt tính năng ghi nhật ký truy cập.

Mở `https://watch.your-domain.org` và nhập mã thông báo bảng điều khiển. Tình trạng sẵn sàng
bao gồm các container; việc cấp chứng chỉ và khả năng kết nối ra bên ngoài phụ thuộc vào DNS
và tường lửa. Nếu HTTPS chưa sẵn sàng, hãy kiểm tra DNS, các quy tắc tường lửa và:

```sh
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

Hình ảnh Caddy được cung cấp nằm ngay sau thẻ `2-alpine`. Khi thực hiện thao tác kéo, hình ảnh đó sẽ được làm mới;
nếu cần các phiên bản cơ sở hạ tầng cố định, hãy ghim một bản tóm tắt đã được kiểm thử vào bản triển khai của bạn.

## Cập nhật và sao lưu

Giữ nguyên tên dự án Compose và khối lượng dữ liệu qua các lần cập nhật. Trước tiên, hãy dừng
trình thu thập dữ liệu và tạo bản sao lưu đầy đủ. Đối với triển khai dựa trên nguồn mặc định:

```sh
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Mỗi lần hãy sử dụng một vị trí sao lưu mới, nằm ngoài kho lưu trữ, và bảo vệ nó như
tài liệu cần quyền truy cập tài khoản. Đường dẫn trong ví dụ chỉ mang tính minh họa; hãy sử dụng vị trí sao lưu riêng tư
của bạn. Sao chép toàn bộ thư mục, bao gồm các tệp ẩn, tất cả các không gian làm việc, khóa,
nhật ký và tệp đa phương tiện. Nếu đã được cấu hình, hãy sao lưu riêng khóa chính của kho lưu trữ bên ngoài.
Tệp ZIP chứa bằng chứng không phải là bản sao lưu ứng dụng có thể khôi phục. Đối với HTTPS, cũng hãy lưu giữ
các khối lượng Caddy nếu bạn cần giữ lại trạng thái chứng chỉ/tài khoản của nó.

Đối với việc triển khai từ nguồn, hãy tải về các tệp bản phát hành mới và chạy lệnh sau:

```sh
docker compose up -d --build --wait
```

Để triển khai hình ảnh, hãy thay đổi `TGWITNESS_IMAGE` thành phiên bản mong muốn, sau đó chạy lệnh:

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Hãy sử dụng (các) tệp Compose của hệ thống cài đặt của bạn cho các lệnh dừng/sao chép ở trên.
Giữ nguyên `.env`, cấu hình tùy chỉnh và tên dự án không thay đổi. `down` giữ lại các
khối lượng có tên; **`down -v` xóa chúng**. Không sao chép `.venv` giữa các hệ điều hành
hoặc các phiên bản Python. Đối với các bản cập nhật gốc, hãy dừng TgWitness, sao lưu toàn bộ thư mục dữ liệu
của nó, thay thế các tệp nguồn và chạy `python start.py --setup-only` trước khi khởi chạy.

Kiểm tra quyền truy cập bảng điều khiển, danh tính tài khoản, trạng thái quan sát và phạm vi bảo hiểm sau khi
cập nhật. Sau khi khởi động lại, TgWitness sẽ tiếp tục từ vị trí cập nhật Telegram đã được lưu và
yêu cầu các bản cập nhật bị bỏ lỡ trong quá trình cập nhật. Việc khôi phục lại có thể
yêu cầu bản sao lưu trước khi cập nhật nếu phiên bản sau này thay đổi định dạng lưu trữ.

## Máy chủ từ xa

Giữ dịch vụ được liên kết với loopback và sử dụng đường hầm SSH, hoặc kết thúc kết nối HTTPS tại một
proxy ngược. Tệp Compose cơ sở chỉ hoạt động trong mạng nội bộ; lớp phủ tùy chọn
`deploy/compose/compose.https.yaml` cung cấp Caddy cho một tên miền đã được cấu hình.
Tránh để token bearer xuất hiện trong URL và nhật ký proxy. Proxy ngược nên giới hạn
kích thước yêu cầu và tần suất kết nối. Không để HTTP thuần túy tiếp xúc với Internet.

Các ví dụ về systemd, tác vụ đăng nhập Windows, trình đại diện người dùng macOS và Caddy được cung cấp
trong thư mục [deploy/](../../deploy/README.md). Hãy kiểm tra và điều chỉnh các đường dẫn của chúng trước khi cài đặt.
Đây là các mẫu được cung cấp sẵn, không phải là các cấu hình nền tảng được thực thi cục bộ. Trình khởi chạy thông thường
không đăng ký bất kỳ dịch vụ nền hay tác vụ nào.

Trên Windows, khi khởi chạy `pythonw.exe` ở chế độ không cửa sổ, các bản ghi chẩn đoán khởi động/máy chủ sẽ được lưu trữ trong
`logs/server.log` trong thư mục dữ liệu (5 MiB mỗi tệp, hai bản sao lưu luân phiên).
Khi khởi chạy ở chế độ giao diện dòng lệnh, hệ thống vẫn lưu giữ nhật ký giao diện dòng lệnh. Tính năng ghi nhật ký truy cập HTTP bị tắt trong cả
hai chế độ. Hãy bảo vệ các tệp nhật ký cùng với thư mục dữ liệu và kiểm tra chúng trước khi chia sẻ.

## Khởi động lại và khoảng trống

Trạng thái quan sát được yêu cầu gần nhất sẽ được lưu lại. Nếu quá trình quan sát đang hoạt động,
hệ thống sẽ cố gắng kết nối lại và tiếp tục theo dõi các nguồn đã chọn khi khởi động. Việc tạm dừng thủ công sẽ xóa
ý định đó. Các lần khởi động lại không thành công sẽ được ghi lại và hiển thị trên bảng điều khiển.

TgWitness lưu trữ vị trí cập nhật của Telegram cho tài khoản và cho từng kênh
(pts, qts, seq và date) trong kho lưu trữ của không gian làm việc và khôi phục chúng khi khởi động lần tiếp theo.
Sau đó, ứng dụng sẽ yêu cầu các bản cập nhật bị bỏ lỡ trong thời gian quá trình bị dừng lại, và
việc kiểm tra lại định kỳ sẽ khôi phục các tin nhắn bị bỏ lỡ và ghi lại những tin nhắn đã được lưu mà Telegram
không còn trả về nữa. Các cuộc hội thoại sẽ được tải lại khi khởi động. Mỗi lần khởi động sẽ ghi lại
đầu nhật ký trước đó, ranh giới ngoại tuyến và vị trí cập nhật mà nó tiếp tục từ đó.
Trình giám sát kiểm tra kết nối mỗi 10 giây và thêm tín hiệu kiểm tra hoạt động mỗi phút
(**Công cụ khác → Thông số → Ghi lại trạng thái hoạt động mỗi**).
Các sự cố ngắt kết nối và khoảng thời gian im lặng được ghi lại dưới dạng khoảng trống trong phạm vi phủ sóng kèm theo lý do.
Các bản chụp lịch sử được lưu trữ dưới dạng các quan sát lịch sử hiện tại riêng biệt bên cạnh các bản ghi trực tiếp.

Hàng đợi phương tiện được lưu trữ trong cơ sở dữ liệu SQLite của từng không gian làm việc. Một tin nhắn và tác vụ tương ứng
được ghi vào cơ sở dữ liệu theo cách nguyên tử. Các tác vụ đang chạy bị gián đoạn sẽ được khôi phục để thử lại khi khởi động.
Mỗi lần tải xuống có thời gian chờ cơ bản là 120 giây cộng với thời gian tính theo tốc độ 256 KiB/s dựa trên kích thước tệp, và
giới hạn từ 1–2.000 MiB cho mỗi loại tệp đính kèm; thời gian chờ, tốc độ và số lần thử lại được cấu hình trong **Công cụ khác → Thông số**. Trình thu thập
sẽ bỏ qua các tệp có kích thước không xác định. Việc tạm dừng sẽ giữ lại các tác vụ đang xếp hàng. Quá trình thử lại sử dụng
mã định danh tệp ban đầu đã được ghi nhận, chứ không bao giờ sử dụng phiên bản mới nhất của tin nhắn đã được chỉnh sửa sau đó.
Các lỗi tạm thời có số lần thử lại giới hạn; việc tạm dừng do quá tải phương tiện (FloodWait) sẽ được duy trì sau khi khởi động lại.
Việc khôi phục phương tiện là riêng biệt với việc khôi phục cập nhật Telegram và không thể tạo lại các tệp đã biến mất.

## Sao lưu, khôi phục và dung lượng

`tgwitness backup FOLDER`
sao chép thư mục dữ liệu trong khi bảng điều khiển vẫn đang chạy:
trước tiên là các điểm kiểm tra, sau đó là các tệp SQLite thông qua API sao lưu trực tuyến, tiếp theo là các khóa, phương tiện và
hồ sơ, do đó không có điểm kiểm tra nào được sao chép mới hơn nhật ký đã sao chép. `backup-manifest.json`
liệt kê mã SHA-256 của từng tệp và các đầu nhật ký. Để khôi phục, hãy dừng TgWitness và thay thế
toàn bộ thư mục dữ liệu bằng thư mục đó. Lần khởi động tiếp theo sẽ ghi lại rằng nhật ký đã được khôi phục
từ một bản sao cũ hơn. Bản ghi đó so sánh nhật ký với đầu nhật ký được lưu trữ trong
`TGWITNESS_STATE_DIR`
, một thư mục bên ngoài thư mục dữ liệu: khối lượng `tgwitness-state`
trong
Compose, `/var/lib/tgwitness-state`
trong các đơn vị systemd, và thư mục trạng thái cục bộ của người dùng
trong các trường hợp khác. Nếu không có thư mục trạng thái có thể ghi, quá trình khôi phục sẽ không được phát hiện và nhật ký sẽ thông báo điều này một lần.

Nếu không có lệnh này, hãy dừng quá trình trước khi sao chép **toàn bộ thư mục dữ liệu**, bao gồm các tệp vault.key,
signing.enc, credentials.enc, cơ sở dữ liệu SQLite và các tệp WAL, phương tiện, token, điểm kiểm tra,
cùng tất cả các thư mục con trong thư mục profiles/. Khôi phục
bản sao hoàn chỉnh trong khi dịch vụ đích đang bị dừng. Việc thiếu khóa vault hoặc
không khớp khóa ký sẽ khiến quá trình khởi động thất bại; không được tái tạo khóa để ép buộc truy cập.

Hãy mã hóa các bản sao lưu bí mật và áp dụng kiểm soát truy cập. Các tệp ZIP chứa bằng chứng là các
tài liệu kiểm tra có thể di chuyển, không phải là bản sao lưu ứng dụng hay bản sao lưu phiên Telegram.
Không có cơ chế xóa tự động theo thời hạn lưu trữ. Hãy dự trù dung lượng đĩa cho tất cả tin nhắn,
siêu dữ liệu thô, tệp đa phương tiện, các tệp xuất tạm thời và các bản sao lưu.

Bắt đầu xác minh và xuất các bản ghi luồng thay vì tải toàn bộ nhật ký.
Quá trình xuất sẽ cố định một bản chụp trạng thái đã đọc trong khi các thao tác ghi WAL mới vẫn có thể tiếp tục; các tác vụ xuất kéo dài
có thể giữ lại các trang WAL, do đó dung lượng đĩa vẫn là yếu tố quan trọng. Các tệp ZIP bị giới hạn ở 4 GiB
khi giải nén để phù hợp với cài đặt mặc định của trình xác minh độc lập; **Công cụ khác → Thông số → Tệp ZIP có chữ ký lớn nhất**
tăng giới hạn này, và các tệp lưu trữ như vậy được xác minh bằng `verify.py --max-gib N`. Các định dạng khác không có giới hạn về số lượng sự kiện.
Các trình duyệt được hỗ trợ truyền các khối phản hồi theo luồng vào tệp do người dùng chọn. Các trình duyệt khác
chỉ đệm tối đa 128 MiB và chuyển các tệp lớn hơn sang CLI đã được xác thực:

~~~sh
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
~~~

Sử dụng `--profile ID` từ **Xuất → ID không gian làm việc** cho một không gian làm việc khác,
`--format zip|jsonl|csv|html`, `--url https://your-server` cho máy chủ từ xa, hoặc
`--max-mib` để thay đổi giới hạn truyền tải 5 GiB. Giao thức HTTP thuần túy chỉ được phép sử dụng cho
loopback. Mã thông báo được truyền qua tiêu đề, các chuyển hướng bị từ chối, các tệp hiện có
không bị ghi đè và các tệp tải xuống chưa hoàn tất sẽ không được công bố là tệp đã hoàn tất.
Nếu TGWITNESS_TOKEN ghi đè lên mã thông báo đã tạo, hãy sử dụng một tệp được bảo vệ riêng
chứa giá trị đang hoạt động đó: panel-token.txt sẽ không bị ghi đè bởi lệnh ghi đè.
SHA-256 của lệnh chỉ là tổng kiểm tra truyền tải; hãy xác minh độc lập tệp ZIP đã ký.

Bảng điều khiển hiển thị các tệp phương tiện đang chờ xử lý/thất bại, tệp phương tiện đang chờ xử lý lâu nhất, dung lượng đĩa trống, các yêu cầu tạm dừng trên Telegram
và các nguồn chưa được xác nhận quyền truy cập. Các chẩn đoán này không phải là
một công cụ giám sát phân phối từ đầu đến cuối hoàn chỉnh. Các không gian làm việc chia sẻ chung một quy trình; một tài khoản gây nhiễu vẫn có thể
ảnh hưởng đến những tài khoản khác. Các quy trình công việc riêng biệt, lưu trữ/xoay vòng, khôi phục cập nhật bền vững
và đánh giá triển khai đầy đủ vẫn được duy trì. Quyền truy cập bảng điều khiển theo phạm vi được ghi chép
trong [quyền truy cập và quyền hạn](../ACCESS.md); các điểm kiểm tra độc lập được đề cập trong
[hướng dẫn chứng kiến](../WITNESS.md).

Các quy trình chi tiết: [kết nối/bảo mật](../CONNECTION-SECURITY.md) và
[chế độ hoạt động](../OPERATIONS.md).
