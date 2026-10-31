# Triển khai

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/deployment/

Vui lòng chạy TgWitness dưới dạng dịch vụ trên Windows, Linux, macOS hoặc Docker, thông qua kết nối HTTPS, kèm theo tính năng sao lưu và cập nhật.

**Tiếng Anh** · [Tiếng Nga](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Tiếng Ukraina](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Tiếng Tây Ban Nha](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Tiếng Bồ Đào Nha (Brazil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Tiếng Thổ Nhĩ Kỳ](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [Tiếng Ả Rập](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [Tiếng Ba Tư](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [Tiếng Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [Tiếng Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Tiếng Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Tiếng Trung giản thể](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Chọn phương thức cài đặt

Đối với gói phần mềm di động, vui lòng giải nén tệp `TgWitness-<version>-windows-amd64-portable.zip` từ GitHub Releases. Đối với các phương pháp khác, vui lòng tải xuống và giải nén tệp ZIP nguồn hoặc sao chép kho lưu trữ, sau đó thực thi lệnh sau từ thư mục dự án:

| Cài đặt | Bắt đầu | Công cụ này có chạy ngầm không? |
| --- | --- | --- |
| Gói phần mềm di động dành cho Windows | `TgWitness.cmd` | Không; hãy giữ cửa sổ mở. |
| Phiên bản dành riêng cho Windows | `Start.cmd` | Không; hãy sử dụng tác vụ đăng nhập tùy chọn để chạy nền. |
| Hỗ trợ bản địa trên Linux/macOS | `sh start.sh` | Không; hãy sử dụng systemd/launchd để chạy nền. |
| Docker trên bất kỳ máy chủ nào được hỗ trợ | `docker compose up -d --build --wait` | Đúng vậy, miễn là daemon Docker vẫn đang chạy. |
| Trợ lý Docker trên Windows | `scripts\Docker.cmd` | Đúng vậy; trình trợ giúp sẽ chờ kiểm tra tình trạng hoạt động của máy chủ web. |
| Trợ lý Docker trên Linux/macOS | `sh scripts/docker-start.sh` | Đúng vậy; trình trợ giúp sẽ chờ kiểm tra tình trạng hoạt động của máy chủ web. |

Đối với máy chủ đám mây mà bên thứ ba có thể kiểm tra — được tạo thông qua API của nhà cung cấp, không sử dụng SSH và chỉ có thể truy cập qua Cloudflare Tunnel — xin tham khảo [phần triển khai có độ tin cậy cao](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md).

Quá trình khởi động gốc sẽ tạo ra một bản `.venv` riêng tư và cài đặt các phụ thuộc đã được ghim sẵn. Docker sẽ xây dựng chúng bên trong hình ảnh, mà không cần Python trên máy chủ. Lần cài đặt đầu tiên cần có kết nối Internet. Khi không tìm thấy Python 3.11 trở lên, `Start.cmd` sẽ hỏi ý kiến người dùng trước khi cài đặt Python 3.12 cho người dùng Windows hiện tại (sử dụng winget, hoặc trình cài đặt từ python.org sau khi xác minh chữ ký của Python Software Foundation); công cụ này tuyệt đối không yêu cầu quyền quản trị viên. Docker và các dịch vụ hệ điều hành vẫn là các điều kiện tiên quyết.

Các bản cài đặt gốc và di động sử dụng `data/live` bên trong thư mục của chúng. Docker sử dụng khối lượng có tên `tgwitness-data` tại `/data`. Đây là các bản cài đặt riêng biệt cho đến khi quý vị chủ động di chuyển toàn bộ thư mục dữ liệu. Xin lưu ý rằng một container Docker mới sẽ không tự động phát hiện các tài khoản gốc.

## Yêu cầu cài đặt

Việc cài đặt bản gốc yêu cầu Python 3.11 trở lên cùng với `venv` và `ensurepip`, kết nối Internet để cài đặt các phụ thuộc ban đầu, và một thư mục dự án có quyền ghi cho `.venv`. Bảng điều khiển đi kèm không cần Node.js hay quá trình xây dựng giao diện người dùng. Vui lòng chạy trình khởi chạy từ tài khoản hệ điều hành thông thường của quý vị; TgWitness không yêu cầu quyền quản trị viên/root.

- **Hệ điều hành Windows:** `Start.cmd` sẽ kiểm tra thư mục `py -3`, sau đó là `python`, tiếp theo là thư mục cài đặt mặc định theo từng người dùng và thư mục Program Files, đồng thời yêu cầu phiên bản 3.11 trở lên. Nếu không có thư mục nào phù hợp, chương trình sẽ đề xuất phương án cài đặt tự động theo từng người dùng như đã mô tả ở trên. `py -3 start.py` cũng hoạt động được. Gói phần mềm di động hoàn toàn không cần Python.
- **Linux:** `start.sh` sẽ thử các phiên bản `python3.13`, `python3.12`, `python3.11`, `python3` và `python`, đồng thời hiển thị lệnh cài đặt tương ứng cho apt, dnf, pacman, zypper, apk hoặc Homebrew nếu không có phiên bản nào đáp ứng yêu cầu. Các hệ thống Debian/Ubuntu có thể cần gói `python3-venv` tương thích với trình thông dịch đã chọn. Phiên bản Python mặc định cũ hơn của hệ điều hành phân phối đó phải được thay thế hoặc bổ sung bằng Python 3.11 trở lên.
- **macOS:** hãy cài đặt bản phân phối Python 3.11+ mới nhất; không nên cho rằng trình thông dịch do hệ điều hành cung cấp đáp ứng yêu cầu. Vui lòng sử dụng tệp `python3 start.py` từ thư mục dự án.
- **Docker:** sử dụng Docker Engine/Desktop với Compose phiên bản 2.20 trở lên. Docker Desktop phải sử dụng các container Linux trên Windows. Container sẽ tự cài đặt các thành phần phụ thuộc Python của riêng mình; máy chủ không cần cài đặt Python riêng biệt.

Vui lòng sử dụng bộ nhớ cục bộ lâu dài cho thư mục dữ liệu. Hãy lập kế hoạch dung lượng dựa trên số lượng tin nhắn, tệp đa phương tiện, tốc độ tăng trưởng của WAL, các bản xuất và bản sao lưu; không có tiêu chuẩn tối thiểu chung nào dựa trên bằng chứng về dung lượng đĩa/RAM áp dụng cho mọi khối lượng công việc. Các kiến trúc CPU và phiên bản Python không có các gói phụ thuộc tương thích có thể yêu cầu các công cụ biên dịch bổ sung cùng với quy trình kiểm định riêng. Thuật ngữ “di động” không phải là tuyên bố về khả năng hỗ trợ phổ quát cho mọi hệ điều hành hay phần cứng.

Hệ điều hành Windows 11 và Python 3.12 đã được xác minh tại máy chủ cục bộ. Các định nghĩa dành cho Linux, macOS và môi trường container cùng quy trình CI đã được cung cấp nhưng chưa được thực thi trên máy chủ phát triển này. Vui lòng tham khảo [tệp VERIFICATION.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/) để biết phạm vi cụ thể.

## Máy tính cục bộ

Vui lòng sử dụng `Start.cmd` trên Windows hoặc `sh start.sh` trên Linux/macOS. `scripts\Setup.cmd` hoặc `sh start.sh --setup-only` sẽ tiến hành chuẩn bị môi trường. Trình khởi chạy sẽ cài đặt các thành phần phụ thuộc khi sử dụng lần đầu; các lần khởi chạy sau đó sẽ tái sử dụng môi trường đã có sẵn. Cần có kết nối Internet để thiết lập và thu thập dữ liệu từ Telegram, tuy nhiên, việc duyệt qua các bản ghi hiện có và tạo tệp xuất vẫn có thể thực hiện ngoại tuyến.

Vui lòng chạy lệnh ``python start.py --check`` sau khi thiết lập để kiểm tra các phụ thuộc cục bộ, Ed25519, bộ nhớ lưu trữ, cấu hình khóa và địa chỉ lắng nghe mà không cần khởi động trình thu thập dữ liệu. Sử dụng lệnh `--json` để nhận kết quả đầu ra có cấu trúc. Chuyển các lệnh `--data-dir`, `--host` và `--port` theo mục đích. Quá trình kiểm tra này không cài đặt gói phần mềm, không tạo nhật ký cũng như không kết nối với Telegram; đây không phải là quá trình đánh giá tính toàn vẹn hay phạm vi bao phủ. Quá trình khởi động sẽ xác minh riêng biệt các nhật ký hiện có. Lệnh `python start.py --help` cũng không yêu cầu cài đặt.

Các tùy chọn:

Sau khi chạy tệp start.py, quý vị hãy thực thi các lệnh phụ trợ bằng lệnh ``.venv\Scripts\python.exe`` trên Windows hoặc ``.venv/bin/python`` trên Linux/macOS, hoặc kích hoạt môi trường đó trước tiên. Các ví dụ ``python -m ...`` dưới đây giả định rằng môi trường đã được kích hoạt.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Các biến môi trường: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE chọn chế độ khóa bên ngoài cho một cài đặt mới; xem phần dưới đây. TGWITNESS_TOKEN, nếu được cung cấp, phải chứa ít nhất 24 ký tự; hãy sử dụng một giá trị ngẫu nhiên được tạo bằng thuật toán mã hóa. Nếu không có thông số này, ứng dụng sẽ tạo ra một mã thông báo ngẫu nhiên 256-bit trong tệp panel-token.txt. Việc ghi đè biến môi trường sẽ không ghi đè lên tệp đó. Vui lòng khởi động lại để luân chuyển thông tin xác thực.

Chỉ có đúng một tiến trình được phép sở hữu một thư mục dữ liệu. Cơ chế khóa tệp trên nhiều nền tảng hệ điều hành sẽ ngăn chặn tình trạng ghi đồng thời vô tình xảy ra. Vui lòng sử dụng một công cụ Uvicorn. Bảng điều khiển có thể quản lý bất kỳ số lượng không gian làm việc nào, với các thư mục không gian làm việc bổ sung nằm trong thư mục profiles/<id>/. Đối với các phiên bản dịch vụ riêng biệt, hãy sử dụng các thư mục và cổng riêng biệt. Các tệp WAL của SQLite phải được lưu trữ trên bộ nhớ lưu trữ cục bộ lâu dài, chứ không phải trên hệ thống tệp mạng. Không được chia sẻ cùng một khối lưu trữ giữa các bản sao.

## Gói phần mềm di động dành cho Windows

Mỗi bản phát hành trên GitHub đều bao gồm `TgWitness-<version>-windows-amd64-portable.zip` và `.sha256` tương ứng. Bản phát hành này chứa phiên bản runtime Python 3.12 chính thức có thể nhúng từ python.org (tổng kiểm tra được cố định trong `tools/build_portable.py`), TgWitness cùng các phụ thuộc được cố định của nó, và ba trình khởi chạy:

| Tệp | Mục đích |
| --- | --- |
| `TgWitness.cmd` | Khởi chạy bảng điều khiển; các tùy chọn bổ sung sẽ được truyền vào, ví dụ: `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Khởi chạy bản demo tổng hợp tại `data\demo` |
| `TgWitness-Check.cmd` | Vui lòng thực hiện kiểm tra sẵn sàng mà không cần khởi động |

Vui lòng giải nén toàn bộ tệp lưu trữ vào một thư mục có quyền ghi như `Documents\TgWitness`; không chạy chương trình từ bên trong tệp ZIP hoặc từ thư mục Program Files. Môi trường chạy sử dụng đường dẫn mô-đun cách ly, do đó các bản cài đặt Python khác và thư mục `PYTHONPATH` sẽ không ảnh hưởng đến nó. Dữ liệu được lưu trữ trong thư mục `data` của gói phần mềm. Để cập nhật, hãy dừng TgWitness, giải nén phiên bản mới vào một thư mục mới và sao chép thư mục `data` sang đó.

Tự xây dựng trên hệ điều hành Windows 64-bit bằng Python 3.12:

```
python tools/build_portable.py
```

Trình xây dựng sẽ xác minh tổng kiểm tra thời gian chạy, cài đặt các phụ thuộc có giới hạn vào gói phần mềm, thực hiện kiểm tra sẵn sàng bằng trình thông dịch nhúng và ghi tệp ZIP cùng tổng kiểm tra vào tệp `dist/`.

## Container

```
docker compose up -d --build --wait
```

Quá trình này sẽ tạo ra một khối lượng lưu trữ cố định có tên cho thư mục /data. Cổng web được ánh xạ đến địa chỉ 127.0.0.1:8787. Quá trình này chạy với UID 10001 cùng các quyền hạn bị giới hạn, hệ thống tệp gốc chỉ đọc, và các thư mục /data và /tmp có thể ghi. `--wait` sẽ kiểm tra tình trạng hoạt động của máy chủ web trước khi trả về kết quả; công cụ này không thiết lập quy trình xác thực hay gửi tin nhắn Telegram. Các hàm trợ giúp được cung cấp sử dụng thời gian chờ sẵn sàng là 180 giây sau khi xây dựng. Quá trình tải xuống các phụ thuộc ban đầu có thể mất nhiều thời gian hơn mức đó.

Cả hai tệp Compose cơ sở đều sử dụng tên dự án `tgwitness`, do đó việc giải nén bản phát hành mới vào một thư mục khác sẽ không tự động chọn một khối dữ liệu mới. Chỉ duy trì một bản triển khai hoạt động cho dự án đó. Đối với các cài đặt độc lập, hãy sử dụng tên `docker compose -p NAME ...` duy nhất cùng cổng máy chủ khác, và giữ nguyên cả hai khi cập nhật. Đối với một bản triển khai cũ hơn sử dụng tên dự án khác, hãy tiếp tục sử dụng tên ban đầu của nó cùng với `-p`; `docker compose ls` liệt kê các dự án hiện có.

Sao chép `deploy/env.example` vào `.env` và thay đổi `TGWITNESS_PORT` để sử dụng một cổng loopback khác. Ví dụ: `TGWITNESS_PORT=8788` hiển thị bảng điều khiển tại `http://127.0.0.1:8788`; container vẫn lắng nghe trên cổng 8787. `.env` bị Git bỏ qua.

Lấy mã thông báo ban đầu:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Các lệnh hữu ích:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` sẽ khởi động lại trình thu thập sau khi xảy ra sự cố hoặc khi daemon Docker được khởi động lại. Trên máy chủ Linux, hãy kích hoạt Docker khi khởi động bằng trình quản lý dịch vụ của bản phân phối hệ điều hành mà quý vị đang sử dụng, thường là `sudo systemctl enable --now docker`. Trên Windows/macOS, hãy kích hoạt cài đặt “khởi động khi đăng nhập” của Docker Desktop. Việc đăng xuất khỏi máy tính để bàn, chuyển sang chế độ ngủ hoặc khi daemon có thể làm gián đoạn quá trình thu thập dữ liệu. Một container bị dừng rõ ràng sẽ vẫn ở trạng thái dừng cho đến khi quý vị khởi động lại nó.

Trong cấu hình ví dụ, dung lượng phân vùng /tmp được giới hạn ở mức 512 MiB. Quá trình xuất dữ liệu sẽ sử dụng khóa `temporary-exports/` của từng không gian làm việc trên phân vùng /data lưu trữ vĩnh viễn thay thế. Vui lòng dành dung lượng tại đó cho các tác vụ xuất dữ liệu đồng thời, sự gia tăng của nhật ký/WAL, tệp phương tiện và bản sao lưu. Trình khởi chạy sử dụng tệp deploy/constraints.txt để cố định các phiên bản phụ thuộc thời gian chạy đáp ứng yêu cầu. Các máy chủ Docker và máy chủ có độ tin cậy cao được cài đặt từ các tệp deploy/requirements.lock và deploy/build.lock bằng lệnh pip --require-hashes: mọi tệp gói phải khớp với mã SHA-256 được ghi lại trong bản cam kết, do đó bất kỳ tệp nào bị thay thế trên PyPI hoặc máy chủ gương sẽ bị từ chối. Hình ảnh cơ sở Python và các gói phần mềm hệ điều hành vẫn cần phải trải qua quá trình kiểm định phiên bản độc lập.

Không sử dụng lệnh `docker compose down -v` trừ khi quý vị có ý định xóa sổ nhật ký và các khóa mã hóa. Báo cáo tình trạng container phản ánh tính khả dụng của máy chủ web, chứ không phải việc ghi lại tin nhắn Telegram thành công. Kiểm tra trạng thái bộ thu thập, tín hiệu hoạt động, lỗi và các sự kiện phạm vi phủ sóng trên bảng điều khiển.

### Hồ sơ nhân chứng độc lập

Dịch vụ `witness` tùy chọn sẽ chạy một [chứng nhân độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/) trong container riêng, với khóa và nhật ký riêng trong khối lượng `witness-data`, đồng thời chỉ cung cấp một mã thông báo chứng nhân chỉ đọc cho bộ thu thập. Quý vị hãy tạo mã thông báo này trên trang **Chứng nhân** của bảng điều khiển, thêm mã thông báo này cùng với mã thông báo bot và kênh vào `.env`, sau đó khởi động cấu hình:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Dịch vụ này kết nối với bộ thu thập (collector) trong mạng Compose tại địa chỉ `http://tgwitness:8787` (`TGWITNESS_WITNESS_COLLECTOR` sẽ ghi đè lên địa chỉ này; ví dụ: `/profiles/<workspace ID>` dành cho một không gian làm việc khác). Đối với tệp chứng cứ (witness) trên một máy chủ riêng biệt do người khác quản lý, quý vị hãy sử dụng `deploy/compose/compose.witness.yaml` tại đó và thiết lập `TGWITNESS_WITNESS_COLLECTOR` thành địa chỉ HTTPS của bộ thu thập; tệp này chỉ chứa duy nhất tệp chứng cứ.

## Cài đặt hình ảnh đã được phát hành

Tính năng này sẽ khả dụng sau khi [quy trình phát hành](https://phishdestroy.github.io/TgWitness/vi/docs/reference/deployment/#automated-github-releases) hoàn tất thành công và cấu hình gói GHCR công khai được thiết lập. Tên/chủ sở hữu của kho lưu trữ không được mã hóa cứng trong cây nguồn này. Vui lòng sử dụng hình ảnh được hiển thị trong phần tóm tắt quy trình phát hành của phiên bản đó.

Sao chép `deploy/env.example` vào `.env`. Đặt `TGWITNESS_IMAGE` thành phiên bản đã được phát hành, bằng cách sử dụng đường dẫn kho lưu trữ **viết thường**, ví dụ:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

Vui lòng chạy tệp này một cách độc lập, thay vì sử dụng tệp `compose.yaml`:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Không cần xây dựng mã nguồn, Python hay trình biên dịch trên máy chủ. Quy trình phát hành nhắm đến các container Linux AMD64 và ARM64, bao gồm cả máy ảo Linux của Docker Desktop. Vui lòng sử dụng thẻ phiên bản hoặc mã `ghcr.io/owner/repository@sha256:...` từ phần tóm tắt quy trình. Không có cấu hình nào cho việc di chuyển thẻ `latest` hay nâng cấp ứng dụng tự động. Các biến thể hình ảnh và mã nguồn sẽ sử dụng cùng một khối lượng dữ liệu khi tên dự án của chúng trùng khớp.

## Tự động kích hoạt HTTPS trên máy chủ

Vui lòng sử dụng máy chủ chạy Docker, một tên miền do quý vị quản lý và bộ nhớ cục bộ lâu dài. Hướng các bản ghi A/AAAA của tên miền đến máy chủ; chỉ công bố bản ghi AAAA nếu địa chỉ IPv6 truy cập được đến máy chủ đó. Cho phép kết nối TCP 80 và 443 từ bên ngoài vào, cũng như kết nối DNS/HTTPS ra bên ngoài để cấp chứng chỉ. Các dịch vụ khác không được chiếm dụng các cổng này trước đó.

Sao chép `deploy/env.example` vào `.env` và thiết lập tên máy chủ, không kèm theo lược đồ hoặc đường dẫn:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

Bắt đầu quá trình biên dịch mã nguồn với lớp phủ HTTPS:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

Đối với hình ảnh đã được đăng tải, vui lòng sử dụng `deploy/compose/compose.image.yaml` làm tệp đầu tiên thay thế. Hãy giữ lại cả hai tham số `-f` để sử dụng cho các lệnh trạng thái, nhật ký, cập nhật và dừng sau này.

Caddy thực hiện việc lấy và gia hạn chứng chỉ, chuyển hướng HTTP sang HTTPS, đồng thời chuyển tiếp các yêu cầu đến bộ thu thập trên mạng Compose riêng tư. Trạng thái chứng chỉ có khối lượng lưu trữ riêng biệt và bền vững. Cổng máy chủ trực tiếp của bộ thu thập vẫn chỉ hoạt động ở chế độ loopback. Cấu hình Caddy được cung cấp không kích hoạt tính năng ghi nhật ký truy cập.

Mở `https://watch.your-domain.org` và nhập mã thông báo bảng điều khiển. Việc chuẩn bị sẵn sàng không xác nhận việc cấp chứng chỉ hoặc khả năng kết nối từ bên ngoài. Nếu HTTPS chưa sẵn sàng, hãy kiểm tra DNS, các quy tắc tường lửa và:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

Hình ảnh Caddy được cung cấp đi kèm với thẻ `2-alpine`. Việc thực hiện lệnh `pull` sẽ cập nhật hình ảnh đó; quý vị có thể ghim một bản tóm tắt đã được kiểm thử vào môi trường triển khai của mình nếu cần sử dụng các phiên bản cơ sở hạ tầng cố định.

## Cập nhật và sao lưu

Giữ nguyên tên dự án Compose và dung lượng dữ liệu qua các bản cập nhật. Trước tiên, hãy dừng trình thu thập dữ liệu và thực hiện sao lưu toàn bộ. Đối với triển khai dựa trên nguồn mặc định:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Hãy sử dụng một đích sao lưu mới mỗi lần, nằm bên ngoài kho lưu trữ, và bảo vệ nó như tài liệu truy cập tài khoản. Đường dẫn ví dụ chỉ mang tính minh họa; quý vị hãy sử dụng vị trí sao lưu riêng tư của mình. Sao chép toàn bộ thư mục, bao gồm các tệp ẩn, tất cả không gian làm việc, khóa, sổ nhật ký và phương tiện truyền thông. Nếu đã cấu hình, hãy sao lưu riêng khóa chính của kho lưu trữ bên ngoài. Tệp ZIP chứa bằng chứng không phải là bản sao lưu ứng dụng có thể khôi phục. Đối với HTTPS, hãy lưu giữ thêm các khối lượng Caddy nếu quý vị cần duy trì trạng thái chứng chỉ/tài khoản của nó.

Để triển khai từ mã nguồn, quý vị hãy tải xuống các tệp bản phát hành mới và thực thi lệnh:

```
docker compose up -d --build --wait
```

Để triển khai phiên bản hình ảnh, quý vị hãy thay đổi `TGWITNESS_IMAGE` thành phiên bản mong muốn, sau đó thực thi lệnh:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Vui lòng sử dụng (các) tệp Compose của bản cài đặt của quý vị cho các lệnh dừng/sao chép nêu trên. Hãy giữ nguyên `.env`, cấu hình tùy chỉnh và tên dự án như cũ. `down` giữ lại các khối dữ liệu được đặt tên; **`down -v` sẽ xóa chúng**. Không sao chép `.venv` giữa các hệ điều hành hoặc các phiên bản Python khác nhau. Để cập nhật bản gốc, hãy dừng TgWitness, sao lưu toàn bộ thư mục dữ liệu của nó, thay thế các tệp nguồn và chạy `python start.py --setup-only` trước khi khởi động.

Vui lòng kiểm tra quyền truy cập bảng điều khiển, thông tin nhận dạng tài khoản, trạng thái quan sát và phạm vi bao phủ sau khi cập nhật. Việc khởi động lại sẽ không khôi phục các bản cập nhật Telegram bị bỏ lỡ. Việc khôi phục về phiên bản trước có thể yêu cầu bản sao lưu trước khi cập nhật nếu phiên bản trong tương lai thay đổi định dạng lưu trữ.

## Các bản phát hành tự động trên GitHub

[Quy trình phát hành](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) đã sẵn sàng để sử dụng sau khi dự án này được đẩy lên kho lưu trữ GitHub có bật tính năng Actions. Quy trình này sẽ được thực thi khi một bản phát hành GitHub được **công bố**, bao gồm cả bản phát hành trước. Việc đẩy bản nháp và thẻ một mình sẽ không dẫn đến việc công bố các gói phần mềm.

1. Vui lòng thiết lập phiên bản gói phần mềm và nhật ký thay đổi, sau đó phát hành bản cập nhật được gắn thẻ `v` cùng với phiên bản `pyproject.toml` chính xác, chẳng hạn như `v0.7.0`.
2. Quy trình làm việc này sẽ xác thực thẻ và thực thi các kiểm tra chung trên trình duyệt Python chia sẻ cho Windows/Linux/macOS, kiểm tra thư mục general/account-import/QR, gói nguồn và Docker. Việc cài đặt bản gốc mới cũng được thực hiện trên cả ba hệ điều hành này bằng Python 3.12.
3. Sau khi vượt qua các bước kiểm tra này, hệ thống sẽ tiến hành kiểm tra sơ bộ (smoke test) hình ảnh ARM64 trên QEMU, đăng tải các hình ảnh AMD64/ARM64 lên `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`, và đính kèm tệp ZIP nguồn, tổng kiểm tra (checksum) cùng gói Python wheel vào bản phát hành. Một tác vụ riêng biệt trên Windows sẽ biên dịch và đính kèm tệp ZIP di động cùng tổng kiểm tra (checksum) của nó.
4. Sau lần xuất bản đầu tiên, quý vị hãy mở cài đặt gói GHCR và thiết lập quyền truy cập thành **Công khai** nếu có ý định tải xuống hình ảnh ẩn danh. Việc chỉ có kho lưu trữ nguồn công khai thôi chưa đảm bảo gói container sẽ được công khai. Chính sách của tổ chức phải cho phép việc xuất bản gói. Quy trình làm việc sử dụng `GITHUB_TOKEN`; không được lưu mật khẩu đăng ký hoặc thông tin đăng nhập VPS trong kho lưu trữ.

Sự thành công của quy trình làm việc từ xa chưa được xác nhận thông qua quá trình chuẩn bị tại địa phương này. Việc mô phỏng ARM64 chỉ là bước kiểm tra sơ bộ, không phải là quá trình kiểm định trên phần cứng gốc hay kiểm định Telegram trong môi trường thực tế. Tính năng này tự động hóa quá trình đóng gói bản phát hành; việc khởi động máy chủ vẫn yêu cầu lệnh Compose cùng các điều kiện tiên quyết về tên miền/máy chủ. Các máy chủ hiện có sẽ không được nâng cấp hoặc khởi động lại tự động khi có bản phát hành mới.

## Máy chủ từ xa

Hãy giữ dịch vụ kết nối với loopback và sử dụng đường hầm SSH, hoặc kết thúc kết nối HTTPS tại một proxy ngược. Tệp Compose cơ bản chỉ hoạt động cục bộ; lớp phủ `deploy/compose/compose.https.yaml` (tùy chọn) cung cấp Caddy cho tên miền đã được cấu hình. Hãy đảm bảo token bearer không xuất hiện trong các URL và nhật ký proxy. Máy chủ proxy ngược nên giới hạn kích thước yêu cầu và tần suất kết nối. Không được để HTTP thuần túy tiếp xúc với Internet.

Các ví dụ về systemd, tác vụ đăng nhập Windows, trình duyệt người dùng macOS và Caddy được cung cấp trong [thư mục deploy/.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Vui lòng kiểm tra và điều chỉnh các đường dẫn này trước khi cài đặt. Đây là các mẫu được cung cấp sẵn, không phải các cấu hình nền tảng được thực thi cục bộ. Không có dịch vụ nền hay tác vụ nào được đăng ký bởi trình khởi chạy thông thường.

Trên hệ điều hành Windows, khi khởi chạy `pythonw.exe` ở chế độ không hiển thị cửa sổ, các thông tin chẩn đoán khởi động/máy chủ sẽ được lưu trữ trong thư mục `logs/server.log` thuộc thư mục dữ liệu (5 MiB mỗi tệp, kèm theo hai bản sao lưu luân phiên). Khi khởi chạy qua giao diện dòng lệnh, hệ thống sẽ lưu lại nhật ký dòng lệnh. Tính năng ghi nhật ký truy cập HTTP bị vô hiệu hóa trong cả hai chế độ. Quý vị cần bảo vệ các tệp nhật ký cùng với thư mục dữ liệu và kiểm tra kỹ lưỡng trước khi chia sẻ.

## Khởi động lại và các khoảng trống

Trạng thái quan sát được yêu cầu gần nhất sẽ được lưu giữ. Nếu quá trình quan sát đang hoạt động, hệ thống sẽ cố gắng kết nối lại và tiếp tục theo dõi các nguồn đã chọn khi khởi động. Việc tạm dừng thủ công sẽ xóa bỏ ý định đó. Các trường hợp khởi động lại không thành công sẽ được ghi lại và hiển thị trên bảng điều khiển.

StringSession duy trì quyền truy cập nhưng không lưu giữ trạng thái cập nhật/thực thể bền vững của Telethon. Các cuộc hội thoại sẽ được tải lại khi khởi động. Telegram/Telethon có thể khôi phục một số sự gián đoạn truyền tải trong khi đang chạy, nhưng TgWitness không đảm bảo khả năng phát lại bền vững sau khi khởi động lại quy trình. Mỗi lần khởi động sẽ ghi lại đầu nhật ký trước đó và ranh giới ngoại tuyến. Trình giám sát kiểm tra kết nối cứ sau 10 giây và thêm tín hiệu kiểm tra hoạt động mỗi phút (**Tham số → Ghi lại trạng thái hoạt động mỗi**). Các sự gián đoạn ngắn có thể bị bỏ sót; việc kết nối kênh truyền tải không đảm bảo việc giao nhận cập nhật hoàn toàn. Các bản chụp nhanh là những quan sát rõ ràng về lịch sử hiện tại, tuyệt đối không phải là việc khôi phục khoảng trống.

Hàng đợi phương tiện được lưu trữ trong cơ sở dữ liệu SQLite của từng không gian làm việc. Một tin nhắn và tác vụ liên quan được cam kết theo cơ chế nguyên tử. Các tác vụ đang chạy bị gián đoạn sẽ được khôi phục để thử lại khi khởi động. Mỗi lần tải xuống có thời gian chờ cơ bản là 120 giây cộng thêm thời gian tính theo tốc độ 256 KiB/s dựa trên kích thước tệp, và giới hạn từ 1–2.000 MiB cho mỗi loại tệp đính kèm; thời gian chờ, tốc độ và số lần thử lại được thiết lập trong **phần Thông số**. Trình thu thập sẽ bỏ qua các tệp có kích thước không xác định. Việc tạm dừng sẽ giữ nguyên các tác vụ đang xếp hàng. Quá trình thử lại sử dụng mã định danh tệp ban đầu đã được ghi nhận, chứ không bao giờ sử dụng phiên bản mới nhất của tin nhắn đã được chỉnh sửa sau đó. Các sự cố tạm thời có số lần thử lại giới hạn; việc tạm dừng FloodWait của phương tiện truyền thông vẫn được duy trì sau khi khởi động lại. Việc khôi phục phương tiện truyền thông là riêng biệt so với việc khôi phục cập nhật Telegram và không thể tái tạo các tệp đã biến mất.

## Sao lưu, khôi phục và dung lượng

Hãy dừng quá trình trước khi sao chép **toàn bộ thư mục dữ liệu**, bao gồm các tệp vault.key, signing.enc, credentials.enc, cơ sở dữ liệu SQLite/tệp WAL, phương tiện truyền thông, mã thông báo, điểm kiểm tra, cùng tất cả các hồ sơ người dùng và thư mục con. Khôi phục bản sao hoàn chỉnh trong khi dịch vụ đích đang bị dừng. Việc thiếu khóa vault hoặc không khớp khóa ký sẽ khiến quá trình khởi động thất bại; không được tái tạo khóa để ép buộc truy cập.

Hãy bảo mật các bản sao lưu bằng cách mã hóa và kiểm soát quyền truy cập. Các tệp ZIP chứa bằng chứng có tính di động cao để xem xét các bằng chứng, chứ không phải là bản sao lưu ứng dụng hay bản sao lưu phiên Telegram. Hệ thống không có tính năng xóa tự động theo thời hạn lưu trữ. Quý vị cần lên kế hoạch về dung lượng đĩa cho tất cả tin nhắn, siêu dữ liệu thô, tệp đa phương tiện, các tệp xuất tạm thời và bản sao lưu.

Khởi động quá trình xác minh và xuất các bản ghi luồng thay vì tải toàn bộ nhật ký. Quá trình xuất sẽ cố định một bản chụp nhanh đã đọc trong khi các thao tác ghi WAL mới vẫn có thể tiếp tục; các tác vụ xuất kéo dài có thể giữ lại các trang WAL, do đó dung lượng đĩa vẫn là yếu tố quan trọng. Các tệp ZIP bị giới hạn ở mức 4 GiB khi giải nén để phù hợp với cài đặt mặc định của bên xác minh độc lập; **Tham số → Tệp ZIP có chữ ký lớn nhất** sẽ nâng giới hạn này lên, và các tệp lưu trữ như vậy sẽ được xác minh bằng `verify.py --max-gib N`. Các định dạng khác không có giới hạn về số lượng sự kiện. Các trình duyệt được hỗ trợ sẽ truyền các khối phản hồi theo luồng vào tệp do người dùng chọn. Các trình duyệt khác sẽ lưu trữ tạm thời tối đa 128 MiB và chuyển các tệp có dung lượng lớn hơn trực tiếp đến CLI đã được xác thực:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Sử dụng `--profile ID` từ **mục Xuất → ID Không gian làm việc** cho một không gian làm việc khác, `--format zip|jsonl|csv|html`, `--url https://your-server` cho máy chủ từ xa, hoặc `--max-mib` để thay đổi giới hạn truyền tải 5 GiB. Giao thức HTTP thuần túy chỉ được phép sử dụng cho loopback. Các mã thông báo được truyền qua tiêu đề, các yêu cầu chuyển hướng sẽ bị từ chối, các tệp hiện có sẽ không bị ghi đè, và các tệp tải xuống chưa hoàn tất sẽ không được công bố như các tệp đã hoàn tất. Nếu TGWITNESS_TOKEN ghi đè lên mã thông báo đã tạo, hãy sử dụng một tệp được bảo vệ riêng biệt chứa giá trị đang hoạt động đó: tệp panel-token.txt sẽ không bị ghi đè bởi giá trị này. Giá trị SHA-256 của lệnh này chỉ là tổng kiểm tra truyền tải; quý vị cần xác minh độc lập tệp ZIP đã được ký.

Các tệp xuất từ máy chủ vẫn được lưu trữ bên trong thư mục riêng tư `temporary-exports/` của từng không gian làm việc. Các tác vụ xuất dữ liệu thành công sẽ tự động xóa các tệp của mình. Các tác vụ xuất bị gián đoạn sẽ bị xóa khi khởi động không gian làm việc tiếp theo, khi khóa phiên bản độc quyền của nó vẫn được duy trì. Thư mục này là một phần của mô hình đe dọa/dung lượng lưu trữ; vui lòng sử dụng một khối dữ liệu được mã hóa. Các hoạt động truyền tải với quy mô sản xuất lên đến nhiều gigabyte vẫn cần được kiểm định trên hệ thống đích của quý vị.

Bảng điều khiển hiển thị các tệp đa phương tiện đang chờ xử lý/thất bại, tệp đa phương tiện đang chờ xử lý lâu nhất, dung lượng đĩa trống, các lần tạm dừng yêu cầu từ Telegram, và các nguồn chưa được xác nhận quyền truy cập. Các chẩn đoán này không phải là một công cụ giám sát việc truyền tải từ đầu đến cuối hoàn chỉnh. Các không gian làm việc chia sẻ chung một quy trình; một tài khoản gây nhiễu vẫn có thể ảnh hưởng đến những tài khoản khác. Các quy trình xử lý riêng biệt, chính sách lưu trữ/xoay vòng, khả năng phục hồi cập nhật bền vững và quy trình đánh giá triển khai đầy đủ vẫn được duy trì. Quyền truy cập bảng điều khiển theo phạm vi được ghi chép trong [phần quyền truy cập và quyền hạn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/); các điểm kiểm tra độc lập được đề cập trong [hướng dẫn dành cho nhân chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/).

## Các tùy chọn kết nối và bảo vệ

Các tuyến kết nối được thiết lập theo từng không gian làm việc và cần được cấu hình trước khi cấp quyền. SOCKS5/HTTP CONNECT sử dụng phụ thuộc python-socks đã được ghim sẵn. MTProxy sử dụng giao thức trung gian ngẫu nhiên đang trong giai đoạn thử nghiệm của Telethon; các khóa bí mật TLS giả mạo không được hỗ trợ. Việc chuyển sang phương án dự phòng trực tiếp phụ thuộc vào [chế độ IP](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/#ip-modes) đã chọn: Chế độ Ẩn IP từ chối tính năng này; chế độ chuyển sang phương án dự phòng rõ ràng cho phép tính năng này sau một khoảng thời gian trì hoãn. Chế độ Đường hầm/VPN cho phép các tuyến đường trực tiếp nhưng không tạo ra mạng VPN. Đây không phải là chính sách mạng áp dụng trên toàn hệ thống.

Đối với các cài đặt mới, biến TGWITNESS_VAULT_KEY_FILE trỏ đến một tệp khóa chính ngẫu nhiên được bảo vệ riêng biệt. Hãy gắn tệp này ở chế độ chỉ đọc bên ngoài thư mục /data trong một container. Hãy bảo quản riêng biệt dữ liệu meta salt công khai trong tệp vault.external.json cho từng không gian làm việc cùng với khóa chính. Các kho lưu trữ cục bộ hiện có cần được di chuyển theo kế hoạch; việc thiết lập biến này sẽ không tự động chuyển đổi chúng. Việc lưu trữ và xuất tin nhắn/tệp đa phương tiện không được mã hóa bởi ứng dụng. Vui lòng sử dụng các phân vùng được mã hóa và không gian lưu trữ tạm thời riêng tư đủ dung lượng khi cần thiết.

Các quy trình chi tiết: [kết nối/bảo mật](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) và [các chế độ hoạt động](https://phishdestroy.github.io/TgWitness/vi/docs/reference/operations/).
