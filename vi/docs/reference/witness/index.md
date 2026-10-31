# Nhân chứng độc lập

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/

Vui lòng chạy một bản sao TgWitness với khóa và bot riêng, đăng các điểm kiểm tra đã được ký lên một kênh và đối chiếu các tệp xuất với các điểm kiểm tra đó.

[Hướng dẫn thiết lập bot và proxy bằng tiếng Nga](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Một bộ thu thập sẽ tự ký vào nhật ký của chính mình, do đó, bất kỳ ai kiểm soát bộ thu thập và khóa của nó về nguyên tắc đều có thể viết lại hoặc cắt bớt nội dung nhật ký rồi ký lại. Witness giúp việc này trở nên có thể phát hiện được. Đây là một quy trình riêng biệt — một container khác, hay chính xác hơn là một máy chủ do người khác vận hành — cứ sau vài phút sẽ truy xuất phần đầu của nhật ký đã được ký bởi bộ thu thập, ký xác nhận những gì nó đã ghi nhận bằng khóa riêng của mình, lưu trữ trong nhật ký của chính nó và đăng lên một kênh Telegram.

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

Mã thông báo được tạo trên trang **Witness** của bảng điều khiển, chỉ hiển thị một lần và được lưu trữ dưới dạng SHA-256. Mã này mở chính xác một điểm cuối, `GET /api/witness/head`, điểm cuối này sẽ trả về một điểm kiểm tra mới được ký cùng với các bộ đếm thu thập không chứa nội dung đã được ký và tình trạng hoạt động. Token này không thể mở bảng điều khiển, đọc nội dung tin nhắn hoặc thay đổi cài đặt, và token bảng điều khiển không được chấp nhận tại đó. Quý vị có thể thu hồi token trên cùng trang này. Bộ thu thập ghi lại thời điểm một khóa chứng nhân mới bắt đầu kiểm tra (`witness.seen`) và hiển thị lần kiểm tra gần nhất cho từng token; một chứng nhân chưa thực hiện kiểm tra trong vòng 2,5 khoảng thời gian sẽ được đánh dấu là quá hạn.

Các nhân chứng mới sẽ gửi một thách thức ngẫu nhiên trong mỗi cuộc thăm dò; tuyên bố ghi lại sẽ lặp lại thách thức đó dưới chữ ký của bộ thu thập. Các bộ đếm được gắn với điểm kiểm tra chính xác và được bao gồm trong các bài đăng có chữ ký của nhân chứng. Các tiêu đề cũ vẫn được nhân chứng độc lập chấp nhận. Việc tăng dung lượng nhật ký đơn thuần không bao giờ được tính là một tin nhắn mới.

## Những nội dung mà công cụ này kiểm tra và ghi lại

Cứ sau mỗi khoảng thời gian (mặc định là 10 phút), công cụ TgWitness sẽ:

1. tự động lấy phần đầu (bộ thu thập không thể đẩy hoặc bỏ qua phần này);
2. xác minh chữ ký của bộ thu thập, khóa bộ thu thập được ghim (`--collector-fingerprint`, hoặc khóa đầu tiên được phát hiện), một số đếm không giảm và một đầu danh sách không thay đổi tại một số đếm không thay đổi;
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

Mở **phần Tiện ích bổ sung → Một bot trong kênh của quý vị → Thiết lập bot** trong bảng điều khiển. Ba bước bao gồm quyền truy cập chỉ đọc, kênh của quý vị và khoảng thời gian, sau đó khởi chạy công cụ chứng thực. Chính sách công bố, proxy HTTP/SOCKS5 tùy chọn và địa chỉ API Bot tùy chỉnh nằm trong **phần Cài đặt nâng cao** . Biểu mẫu sẽ tải xuống tệp `witness.json` với khóa thu thập dữ liệu của không gian làm việc này được ghim sẵn. Vui lòng tải xuống mã thông báo chỉ đọc vừa được tạo với tùy chọn **“Lưu tệp truy cập** dưới dạng `witness-token.txt` ”; đặt tệp này cùng với tệp `bot-token.txt` được tạo trên máy chủ chứng thực bên cạnh tệp JSON đó. Bộ thu thập dữ liệu sẽ không bao giờ nhận được mã thông báo của bot. Việc tải xuống sẽ không khởi động dịch vụ hay xuất bản bất kỳ thông điệp nào. Không có chứng nhân dự án được lưu trữ nào được đăng ký một cách ngầm định.

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

Địa chỉ thu thập, mã thông báo và kênh đến từ `--collector`, `--token` hoặc `--token-file`, `--bot-token` hoặc `--bot-token-file` và `--channel`, hoặc `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` và `_CHANNEL`, giúp giữ bí mật khỏi danh sách quy trình.

Một tệp cấu hình sử dụng các tên tùy chọn có dấu gạch dưới, kèm theo chuỗi ký tự `texts` để thay thế các từ trong các bài đăng trên kênh:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Các khóa `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Dòng lệnh có ưu tiên cao hơn môi trường, còn môi trường lại có ưu tiên cao hơn tệp tin. Các tùy chọn hoặc khóa văn bản không xác định sẽ khiến công cụ ngừng hoạt động kèm theo thông báo thay vì bị bỏ qua. Cách diễn đạt không bao giờ ảnh hưởng đến quá trình xác minh: tệp verify.py sẽ kiểm tra mã thông báo đã được ký số ở cuối mỗi bài đăng. Với `--post changes` hoặc `problems`, các kiểm tra chưa được đăng vẫn nằm trong sổ nhật ký chứng nhân và `verify.py` liệt kê chúng là chưa từng được đăng; bản ghi đầu tiên nêu rõ chính sách. Mọi kiểm tra vẫn xuất hiện trong sổ nhật ký, do đó số lần đăng ít hơn đồng nghĩa với việc có ít thời điểm Telegram độc lập hơn, chứ không phải số lượng kiểm tra ít hơn.

Ngay cả khi không có kênh, TgWitness vẫn duy trì nhật ký của mình. Vui lòng lưu giữ dấu vân tay khóa của TgWitness (`python -m tgwitness.witness fingerprint`) ở một nơi khác.

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

Cờ này đảm bảo tính nhất quán với các bản ghi chứng cứ được cung cấp và ghim sẵn. Người vận hành vẫn phải xác minh tính độc lập của bên chứng thực và lưu trữ các bản ghi của bên này một cách riêng biệt. Cờ này không xác nhận tính xác thực của tin nhắn, tính đầy đủ của bộ sưu tập hay thời gian hoạt động được đo lường độc lập.

Một bản chứng cứ cho thấy những gì bộ thu thập đã báo cáo tại các thời điểm đó và rằng các bản xuất sau này phù hợp với thông tin đó. Nó không chứng minh rằng bộ thu thập đã ghi lại toàn bộ nội dung mà Telegram gửi đến, hay rằng nội dung tin nhắn là đúng sự thật. Một bản chứng cứ được chạy bởi cùng một người vận hành trên cùng một máy tính sẽ có độ tin cậy thấp hơn so với bản được chạy bởi người khác.

Chỉ riêng việc tăng số lượng không thể đảm bảo tính liên tục “chỉ thêm” trên mạng: việc so sánh ngoại tuyến phải đối chiếu từng giá trị băm tiền tố được lưu giữ với bản xuất đầy đủ từ bộ thu thập. Thời gian ngừng hoạt động của Witness và các sự cố không xuất bản sẽ để lại những khoảng trống không có điểm neo bên ngoài. Các bài đăng bị thiếu có thể được báo cáo dựa trên sổ nhật ký Witness đã được lưu giữ; cả kênh lẫn máy chủ do cùng một nhà điều hành kiểm soát đều không phải là kho lưu trữ bên thứ ba bất biến.
