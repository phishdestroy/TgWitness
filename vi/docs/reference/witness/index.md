# Nhân chứng độc lập

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/

Vui lòng chạy một bản sao TgWitness với khóa và bot riêng, đăng các điểm kiểm tra đã được ký lên một kênh và đối chiếu các tệp xuất với các điểm kiểm tra đó.

[Xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/) · [Độ tin cậy cao](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/) · [Hướng dẫn sử dụng bảng điều khiển](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

Sơ đồ quy trình · Trình thu thập → Witness (điểm kiểm tra có chữ ký: số lượng bản ghi + băm tiêu đề); Witness → Sổ nhật ký chứng cứ, khóa riêng; Witness → Kênh Telegram (bài đăng có chữ ký được gửi qua bot riêng của nền tảng này); Tệp ZIP chứa bằng chứng → verify.py; Sổ nhật ký chứng cứ, khóa riêng → verify.py; Kênh Telegram → verify.py (Tính năng xuất dữ liệu từ Telegram Desktop hoặc trang t.me/s) · Trình thu thập · Witness · Sổ nhật ký chứng cứ, khóariêng · Kênh Telegram · Tệp ZIP chứa bằng chứng · verify.py · điểm kiểm tra có chữ ký: số · lượng bản ghi + băm tiêu đề · bài đăng có chữ ký được gửi · qua bot riêng của nền tảng · này · Tính năng xuất dữ liệu từ · Telegram Desktop hoặc trang · t.me/s

**Sơ đồ dưới dạng văn bản**

1. Trình thu thập → Witness (điểm kiểm tra có chữ ký: số lượng bản ghi + băm tiêu đề)
2. Witness → Sổ nhật ký chứng cứ, khóa riêng
3. Witness → Kênh Telegram (bài đăng có chữ ký được gửi qua bot riêng của nền tảng này)
4. Tệp ZIP chứa bằng chứng → verify.py
5. Sổ nhật ký chứng cứ, khóa riêng → verify.py
6. Kênh Telegram → verify.py (Tính năng xuất dữ liệu từ Telegram Desktop hoặc trang t.me/s)

## Những gì TgWitness cung cấp và những gì nó không cung cấp

| Người làm chứng đã | Người làm chứng chưa bao giờ |
| --- | --- |
| Một **mã thông báo chứng thực** chỉ đọc dành cho một không gian làm việc | Phiên làm việc Telegram hoặc thông tin đăng nhập API của người thu thập dữ liệu |
| Sử dụng khóa Ed25519 và sổ nhật ký riêng | Kho lưu trữ của bộ thu thập, khóa ký hoặc mã thông báo bảng điều khiển |
| Mã thông báo bot Telegram riêng của nền tảng này | Nội dung tin nhắn: phần đầu bao gồm số lượng bản ghi và mã băm |

Token được tạo trong **Extras → Independent witness**, chỉ hiển thị một lần và chỉ được lưu trữ dưới dạng SHA-256. Nó mở chính xác một điểm cuối, `GET /api/witness/head`, trả về một điểm kiểm tra vừa được ký cùng với các bộ đếm bộ sưu tập không chứa nội dung đã được ký và tình trạng hoạt động. Nó không thể mở bảng điều khiển, đọc nội dung tin nhắn hoặc thay đổi cài đặt, và token bảng điều khiển không được chấp nhận tại đó. Hủy token trên cùng trang. Trình thu thập ghi lại thời điểm một khóa chứng nhân mới bắt đầu kiểm tra (`witness.seen`) và hiển thị lần kiểm tra gần nhất cho mỗi mã thông báo; một nhân chứng chưa kiểm tra trong vòng 2,5 khoảng thời gian sẽ được đánh dấu là quá hạn.

Các nhân chứng mới sẽ gửi một thách thức ngẫu nhiên trong mỗi cuộc thăm dò; tuyên bố ghi lại sẽ lặp lại thách thức đó dưới chữ ký của bộ thu thập. Các bộ đếm được gắn với điểm kiểm tra chính xác và được bao gồm trong các bài đăng có chữ ký của nhân chứng. Các tiêu đề cũ vẫn được nhân chứng độc lập chấp nhận. Việc tăng dung lượng nhật ký đơn thuần không bao giờ được tính là một tin nhắn mới.

## Những nội dung mà công cụ này kiểm tra và ghi lại

Cứ sau mỗi khoảng thời gian (mặc định là 10 phút), công cụ TgWitness sẽ:

1. tự động lấy phần đầu (bộ thu thập không thể đẩy hoặc bỏ qua phần này);
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
3. ghi thêm một bản ghi đã được ký vào nhật ký của chính nó: `witness.anchor` với trạng thái `ok`, `key_changed`, `rollback` (số lượng bản ghi ít hơn trước), `fork` (độ dài tương tự, tiêu đề khác ) hoặc `invalid` (câu trả lời không qua được quá trình xác minh), hoặc `witness.no_response` khi bộ thu thập không phản hồi;
4. đăng kết quả lên kênh, kèm chữ ký, bao gồm cả trường hợp “không có phản hồi” trong khi TgWitness đang hoạt động và có thể kết nối với Bot API. ID bài đăng được ghi lại (`witness.posted`), kể cả khi việc đăng không thành công (`witness.post_failed`).

Một bài đăng trông như sau; dòng cuối cùng chứa tuyên bố đã được ký xác nhận:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Chạy công cụ Witness

Quý vị cần một bot Telegram (tạo bot bằng @BotFather), một kênh mà bot đó là quản trị viên, và địa chỉ của bộ thu thập phải có thể truy cập được từ phía người làm chứng — qua HTTPS bên ngoài mạng riêng (xem cấu hình HTTPS trong [phần triển khai](https://phishdestroy.github.io/TgWitness/vi/docs/reference/deployment/)).

Mở **Extras → Independent witness → Configure** trong bảng điều khiển. Ba bước bao gồm quyền truy cập chỉ đọc, kênh của bạn và khoảng thời gian, sau đó khởi chạy công cụ chứng thực. Chính sách xuất bản, proxy HTTP/SOCKS5 tùy chọn và địa chỉ API Bot tùy chỉnh nằm trong **phần Cài đặt nâng cao**. Biểu mẫu sẽ tải xuống `witness.json` với khóa thu thập dữ liệu của không gian làm việc này được gắn sẵn. Tải xuống mã thông báo chỉ đọc vừa tạo bằng cách chọn **“Lưu tệp truy cập** dưới dạng” `witness-token.txt`; đặt nó cùng với một `bot-token.txt`được tạo trên máy chủ chứng nhân bên cạnh tệp JSON đó. Bộ thu thập không bao giờ nhận được mã thông báo bot. Việc tải xuống không khởi động dịch vụ hoặc xuất bản tin nhắn. Không có chứng nhân dự án được lưu trữ nào được đăng ký ngầm.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

Lệnh đầu tiên kiểm tra các tệp cấu hình và tệp bí mật mà không cần thực hiện yêu cầu mạng hay tạo khóa . Các đường dẫn trong JSON là đường dẫn tương đối so với tệp đó; các đường dẫn CLI/môi trường là đường dẫn tương đối so với thư mục làm việc. Lưu giữ dấu vân tay của chứng nhân bên ngoài máy chủ của nó. Chỉ báo lần lấy mẫu cuối cùng của bộ thu thập chỉ xác nhận yêu cầu; việc công bố được báo cáo bởi Proof hoặc được kiểm tra trong nhật ký chứng nhân và kênh.

Nếu bảng điều khiển nằm phía sau một đường hầm SSH, vui lòng chỉ công khai điểm cuối chứng cứ trong phạm vi trên một tên miền HTTPS riêng biệt theo [ví dụ về Caddy này](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). Không gian làm việc mặc định sẽ sử dụng `https://witness.example.org`, các không gian làm việc khác sử dụng `https://witness.example.org/profiles/ID`. Vẫn cần có mã thông báo; bảng điều khiển và các đường dẫn API khác của nó sẽ không được chuyển tiếp qua máy chủ ảo đó.

Vui lòng chọn `all` để nhận các điểm kiểm tra được công bố định kỳ. Khoảng thời gian năm phút tương đương với khoảng 288 bài đăng mỗi không gian làm việc mỗi ngày. `changes`/`problems` cố ý không công bố một số điểm kiểm tra. MTProxy dành cho ứng dụng Telegram của người thu thập dữ liệu. Việc thăm dò HTTP của Witness và API Bot HTTPS của Telegram sử dụng các tuyến đường riêng biệt: trực tiếp/HTTP/SOCKS5 ([API Bot](https://core.telegram.org/bots/api)).

**Bên cạnh trình thu thập dữ liệu, khi sử dụng Docker** (cùng một máy chủ — quy trình và khóa độc lập, nhưng cùng một người vận hành): hãy nhập các giá trị vào `.env` và khởi động cấu hình.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

Khi sử dụng hình ảnh đã được công bố, vui lòng ghi rõ mã `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**Trên máy chủ của bên thứ ba** (một nhân chứng độc lập thực sự): sao chép kho lưu trữ vào đó, thiết lập `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` cùng với ba giá trị nêu trên vào `.env`, sau đó

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

hoặc không sử dụng Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Đăng lên Discord

Một nhân chứng có thể đăng lên kênh Discord thay vì Telegram. Trong Discord, mở **Chỉnh sửa kênh → Tích hợp → Webhooks**, tạo một webhook và sao chép URL của nó. Trong bảng điều khiển, chọn **webhook Discord · kênh của bạn** ở bước 2. Trên máy chủ của nhân chứng, lưu URL này dưới tên `discord-webhook.txt` bên cạnh `witness.json`; nó sẽ không bao giờ đến được bộ thu thập.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

Một nhân chứng có một nhà xuất bản: một kênh Telegram hoặc một webhook Discord, không phải cả hai. Các bài đăng đều chứa cùng một tuyên bố đã được ký và không thể gửi thông báo đến bất kỳ ai. Một bài đăng dài hơn giới hạn 2.000 ký tự của Discord sẽ được thay thế bằng một dòng ngắn kèm theo bản kiểm tra đầy đủ dưới dạng `witness-check.txt`. Mỗi ID bài đăng được ghi lại dưới dạng `witness.posted`. `verify.py --channel`chỉ đọc các tệp xuất từ kênh Telegram, vì vậy đối với Discord, hãy giữ nhật ký chứng nhân: nó chứa mọi bản kiểm tra.

### Các tùy chọn

| Tùy chọn | Môi trường | Mặc định | Ý nghĩa |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Khoảng thời gian giữa các lần kiểm tra: 1–1.440 |
| `--timeout` | `_TIMEOUT` | 30 | Thời gian chờ cho trình thu thập dữ liệu và Bot API: từ 5 đến 600 giây |
| `--post` | `_POST` | `all` | `all`: mọi kiểm tra; `changes`: một hướng đi mới hoặc một vấn đề; `problems`: chỉ có vấn đề và những câu trả lời còn thiếu |
| `--title` | `_TITLE` | `TgWitness witness` | Những từ đầu tiên trong mỗi bài đăng trên kênh |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Hãy lưu lại khóa thu thập thay vì tin tưởng vào câu trả lời đầu tiên |
| `--proxy` | `_PROXY` | trực tiếp | `socks5://host:port` hoặc `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Địa chỉ API Bot, ví dụ: một máy chủ API Bot cục bộ |
| `--data-dir` | `_DATA` | `witness-data` | Khóa chứng thực và nhật ký |
| `--config` | `_CONFIG` | – | Tệp JSON với bất kỳ tùy chọn nào nêu trên |

Địa chỉ bộ thu thập, mã thông báo và kênh đến từ `--collector`, `--token` hoặc `--token-file`, `--bot-token` hoặc `--bot-token-file`, `--discord-webhook-file` và `--channel`, hoặc `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` và `_CHANNEL`, giúp giữ các bí mật khỏi danh sách quy trình.

Một tệp cấu hình sử dụng các tên tùy chọn có dấu gạch dưới, kèm theo chuỗi ký tự `texts` để thay thế các từ trong các bài đăng trên kênh:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Các khóa `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Dòng lệnh có ưu tiên cao hơn môi trường, còn môi trường lại có ưu tiên cao hơn tệp tin. Các tùy chọn hoặc khóa văn bản không xác định sẽ khiến công cụ ngừng hoạt động kèm theo thông báo thay vì bị bỏ qua. Cách diễn đạt không bao giờ ảnh hưởng đến quá trình xác minh: tệp verify.py sẽ kiểm tra mã thông báo đã được ký số ở cuối mỗi bài đăng. Với `--post changes` hoặc `problems`, các kiểm tra chưa được đăng vẫn nằm trong sổ nhật ký chứng nhân và `verify.py` liệt kê chúng là chưa từng được đăng; bản ghi đầu tiên nêu rõ chính sách. Mọi kiểm tra vẫn xuất hiện trong sổ nhật ký, do đó số lần đăng ít hơn đồng nghĩa với việc có ít thời điểm Telegram độc lập hơn, chứ không phải số lượng kiểm tra ít hơn.

Ngay cả khi không có kênh, TgWitness vẫn duy trì nhật ký của mình. Vui lòng lưu giữ dấu vân tay khóa của TgWitness (`python -m tgwitness.witness fingerprint`) ở một nơi khác.

## Trang chứng minh công khai cho một số không gian làm việc

`python -m tgwitness.proof` TgWitness hỗ trợ tối đa 32 không gian làm việc cùng lúc và cung cấp một trang chỉ đọc với bản kiểm tra đã ký mới nhất của từng không gian. Mỗi không gian làm việc có khóa chứng thực riêng và sổ nhật ký trong thư mục dữ liệu, cùng với một khóa thu thập được ghim; việc đăng lên kênh Telegram là tùy chọn cho từng không gian làm việc. Bắt đầu từ [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| Lĩnh vực | Ý nghĩa |
| --- | --- |
| `title` | Tiêu đề trang, 1–100 ký tự |
| `data_dir` | Khóa và nhật ký Witness, liên quan đến tệp; mặc định `proof-data` |
| `interval`, `timeout` | Số phút giữa các lần kiểm tra (1–1440, mặc định là 5); số giây chờ (5–600, mặc định là 20) |
| `workspaces[].id`, `label` | Biệt danh viết thường ngắn và tên hiển thị |
| `workspaces[].collector` | Địa chỉ Collector; các không gian làm việc khác kết thúc bằng `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Bắt buộc, khác nhau tùy theo từng không gian làm việc |
| `workspaces[].token_file` | Tệp chứa mã chứng thực chỉ đọc của không gian làm việc đó |
| `workspaces[].channel`, `bot_token_file` | Tùy chọn, kết hợp: đăng mỗi lần kiểm tra lên một kênh |
| `workspaces[].proxy`, `bot_api` | Đường dẫn tùy chọn và địa chỉ API Bot |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

Lệnh đầu tiên xác thực tệp và các tệp token mà không cần thiết lập kết nối. Trang này chỉ phản hồi các yêu cầu GET và HEAD:

- `/` hiển thị tất cả các không gian làm việc; một không gian làm việc không được kiểm tra trong 2,5 khoảng thời gian sẽ được đánh dấu là đã hết hạn.
- `/api/proof` trả về kết quả giống như JSON.
- `/api/proof/<id>` tải xuống bản tuyên bố đã ký mới nhất (`tgwitness-public-proof-v1`): số bản ghi chứng thực và mã băm, trạng thái, khóa thu thập được ghim, điểm kiểm tra, số lần thu thập và liệu bài đăng trên kênh có thành công hay không, được ký bằng khóa chứng thực của không gian làm việc đó.
- `/healthz` Trả về mã lỗi 503 khi trình giám sát của không gian làm việc đã ngừng hoạt động.

Đặt tên máy chủ riêng cho trang, ví dụ như [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). Để xác minh, hãy xuất sổ nhật ký chứng thực của không gian làm việc bằng `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` và sử dụng nó theo hướng dẫn dưới đây.

## Xác minh

Về phía người làm chứng, hãy xuất nhật ký của họ:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Sau đó, tại bất kỳ đâu, với tệp ZIP đã được ký bởi trình thu thập và kênh được xuất từ Telegram Desktop (*Chọn “Xuất lịch sử trò chuyện* ” → “JSON” sẽ cho ra mã `result.json` ) hoặc trang công khai `https://t.me/s/…` của kênh đó:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` sẽ kiểm tra nhật ký chứng cứ (chuỗi và chữ ký), sau đó xác minh rằng **mọi tiêu đề mà chứng nhân đã quan sát đều nằm trong nhật ký đã xuất**: bản ghi tại vị trí đếm đó phải có chính xác giá trị băm đó. Một tiêu đề không khớp sẽ không qua được quá trình xác minh — điều này có nghĩa là nhật ký đã bị thay đổi sau khi chứng nhân quan sát nó. Nó cũng báo cáo các tiêu đề được chứng kiến sau khi xuất, các bất thường mà nhân chứng đã ghi lại, các câu trả lời không thành công, các khoảng thời gian có các điểm kiểm tra khớp nhau hiện diện trong bản xuất này (“Được chứng kiến từ X đến Y”) và các khoảng trống. Các điểm kiểm tra sau đó không mở rộng các khoảng thời gian đó. Kết quả bao gồm số bản ghi khớp cuối cùng và số lượng bản ghi còn lại không có điểm kiểm tra khớp. Chỉ các câu trả lời được ký bằng chính khóa của bản xuất mới được tính: một bản xuất được ký bằng khóa mà nhân chứng chưa từng nhìn thấy sẽ được báo cáo là chưa được chứng kiến, và nếu không có `--fingerprint`, người ký sẽ vẫn chưa được xác định. Với `--channel`, mỗi bài đăng được ký phải khớp với nhật ký của người làm chứng theo từng bản ghi: các bài đăng bị thay đổi sẽ không qua được quá trình xác minh, các bài đăng bị thiếu sẽ được liệt kê. Ngày tháng trong tệp xuất JSON Telegram được cung cấp là siêu dữ liệu có thể chỉnh sửa, nằm ngoài mã thông báo người làm chứng đã ký. Việc khớp với mã thông báo không xác thực ngày xuất bản; kết quả báo cáo rõ ràng rằng việc xác minh thời gian xuất bản đã không được thực hiện.

### Yêu cầu giới hạn xuất dữ liệu có chứng thực

Đối với các trường hợp bàn giao bắt buộc phải kèm theo bản ghi cuối cùng có chứng kiến, vui lòng thêm mã `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Điều này yêu cầu phải có dấu vân tay chứng nhân được lưu giữ độc lập và một điểm kiểm tra khớp tại chính xác điểm kết thúc của quá trình xuất này. Một điểm kiểm tra chỉ bao phủ một tiền tố trước đó là không đủ. Hãy tạm dừng việc thu thập, để chứng nhân quan sát trạng thái cuối cùng, và tiến hành xuất trước khi có thêm các ghi chép vào nhật ký; nếu nhật ký thay đổi, hãy lưu giữ một điểm kiểm tra khác và xuất trạng thái đó. Chỉ riêng điểm kiểm tra sau đó không thể xác minh hàm băm cuối cùng của một tệp xuất ngắn hơn. Khi cờ `--channel` cũng được cung cấp, việc thiếu các bài đăng được tuyên bố hoặc tập kết quả khớp trống sẽ khiến quá trình này không vượt qua được kiểm tra nghiêm ngặt này. Nếu không có cờ này, các kiểm tra tính toàn vẹn thông thường vẫn báo cáo các bản ghi chưa được chứng kiến mà không từ chối một kho lưu trữ vốn vẫn còn nguyên vẹn.

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.
