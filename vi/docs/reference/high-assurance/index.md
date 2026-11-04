# Triển khai có độ tin cậy cao

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/

Một máy chủ được bảo mật 24/7 trên Hetzner hoặc Phala Cloud, Gateway DNS và các kiểm tra mà bên thứ ba có thể lặp lại.

Một nhật ký đã được ký xác nhận chứng minh rằng các bản ghi không bị thay đổi **sau khi** ký. Đối với các trường hợp nghiêm trọng, câu hỏi tiếp theo là liệu có ai đó có thể đã can thiệp vào dữ liệu **trước** khi nó được ký hay không: ai đã chạy trình thu thập dữ liệu, trên máy nào, và liệu có ai đã đăng nhập vào nó hay không. Chế độ tùy chọn này triển khai trình thu thập dữ liệu sao cho một bên thứ ba có thể kiểm tra điều đó, bằng cách sử dụng các bản ghi được lưu trữ bởi nhà cung cấp dịch vụ đám mây và Cloudflare thay vì chỉ dựa vào lời khẳng định của nhà điều hành.

Việc sử dụng thông thường trên máy cục bộ và Docker vẫn không thay đổi. Không có gì ở đây hoạt động trừ khi bạn triển khai bằng `python -m tgwitness.cloud`, và trình thu thập dữ liệu chỉ đọc máy chủ của nó khi quá trình triển khai được thiết lập `TGWITNESS_ASSURANCE`.

Sơ đồ quy trình · Người vận hành → Máy chủ, tường lửa không có quy tắc cho lưu lượng vào (API nhà cung cấp); Người vận hành → Tunnel và DNS (API Cloudflare); Máy chủ, tường lửa không có quy tắc cho lưu lượng vào → Tunnel và DNS (chỉ gửi đi); Máy chủ, tường lửa không có quy tắc cho lưu lượng vào → Khóa ký được tạo trên máy chủ; Verifier, các token chỉ đọc → Nhật ký nhà cung cấp và tường lửa; Verifier, các token chỉ đọc → Địa chỉ kết nối đường hầm và cổng vào; Verifier, các token chỉ đọc → Tuyên bố /api/assurance đã được ký; Verifier, các token chỉ đọc → Tệp ZIP chứa bằng chứng · Người vận hành · Verifier, các token chỉđọc · Máy chủ, tường lửa khôngcó quy tắc cho lưu lượngvào · Nhật ký nhà cung cấp vàtường lửa · Địa chỉ kết nối đường hầmvà cổng vào · Tuyên bố /api/assurance đãđược ký · Tệp ZIP chứa bằng chứng · Tunnel và DNS · Khóa ký được tạo trên máychủ · API nhà cung cấp · API Cloudflare · chỉ gửi đi

**Sơ đồ dưới dạng văn bản**

1. Người vận hành → Máy chủ, tường lửa không có quy tắc cho lưu lượng vào (API nhà cung cấp)
2. Người vận hành → Tunnel và DNS (API Cloudflare)
3. Máy chủ, tường lửa không có quy tắc cho lưu lượng vào → Tunnel và DNS (chỉ gửi đi)
4. Máy chủ, tường lửa không có quy tắc cho lưu lượng vào → Khóa ký được tạo trên máy chủ
5. Verifier, các token chỉ đọc → Nhật ký nhà cung cấp và tường lửa
6. Verifier, các token chỉ đọc → Địa chỉ kết nối đường hầm và cổng vào
7. Verifier, các token chỉ đọc → Tuyên bố /api/assurance đã được ký
8. Verifier, các token chỉ đọc → Tệp ZIP chứa bằng chứng

## Những gì người xác minh có thể kiểm tra

| Tuyên bố | Cách kiểm tra | Quản lý bởi |
| --- | --- | --- |
| Máy chủ đã được tạo thông qua API của nhà cung cấp vào một thời điểm cụ thể | Đối tượng máy chủ và quá trình tạo ra nó trong nhật ký riêng của nhà cung cấp | Nhà cung cấp |
| Không ai sử dụng các đường dẫn truy cập của nhà cung cấp | Nhật ký các yêu cầu trên bảng điều khiển, khôi phục, đặt lại mật khẩu, xây dựng lại, ISO, hình ảnh, bản sao lưu | Nhà cung cấp |
| Không có gì có thể kết nối với nó | Tường lửa của nhà cung cấp không có quy tắc cho phép kết nối vào; SSH bị ẩn ngay từ lần khởi động đầu tiên | Nhà cung cấp (tường lửa), máy chủ (SSH) |
| Bảng điều khiển chỉ có thể truy cập thông qua đường hầm | Lưu lượng vào đường hầm chỉ được chuyển tiếp đến bảng điều khiển; trình kết nối chạy từ địa chỉ máy chủ | Cloudflare |
| Chính phần mềm này đang chạy | Hash cây nguồn đã ký của trình thu thập tương đương với bản checkout của commit đã được triển khai | Collector, được kiểm tra dựa trên Git |
| Khóa ký đã được tạo trên máy chủ đó | Khóa này ký một tuyên bố nêu rõ ID máy chủ của nhà cung cấp và giá trị băm của tệp cloud-init mà nó đã nhận được | Collector, đã được kiểm tra với nhà cung cấp |
| Nhật ký này thuộc về khóa và máy chủ đó | Mỗi quá trình bắt đầu trong bằng chứng ZIP đều chứa thông số đo lường máy chủ cho máy chủ đó | Bằng chứng ZIP |

Các số liệu máy chủ (trình nghe SSH và các tiến trình, phiên hiện tại, các lần đăng nhập `wtmp`, quá trình khởi động) được chính bộ thu thập báo cáo và được ký vào mỗi lần khởi động tiến trình cũng như vào `host.state` bản ghi mỗi khi chúng thay đổi. Người dùng root trên máy chủ có thể làm sai lệch các số liệu này; chúng hỗ trợ các bản ghi của nhà cung cấp và Cloudflare thay vì thay thế chúng.

## Nhà cung cấp

| `--provider` | Thông tin đăng nhập | Quyền truy cập chỉ đọc của Verifier | Nhật ký nhà cung cấp dành cho người xác minh | Dành cho |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Token đọc của cùng dự án | Các hành động liên quan đến máy chủ và tường lửa | Trong khi các tài nguyên vẫn còn tồn tại |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Mã truy cập cá nhân chỉ đọc | Các hành động của Droplet | Trong khi Droplet vẫn tồn tại |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` phạm vi chỉ đọc | Sự kiện tài khoản, phiên bản quy tắc tường lửa | 90 ngày |
| `vultr` | `VULTR_API_KEY` | Người dùng có quyền truy cập đọc và `activity_logs` quyền | Nhật ký hoạt động tài khoản (phương thức, đường dẫn, tác nhân) | 30 ngày, thời gian lưu trữ có thể kéo dài hơn nếu đăng ký dịch vụ nhật ký kiểm toán |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | Lịch sử sự kiện CloudTrail | 90 ngày |
| `phala` | `PHALA_CLOUD_API_KEY` | Một khóa API của cùng một không gian làm việc | Các bản cập nhật ứng dụng: thay đổi cấu hình và môi trường, khởi động lại, nâng cấp hệ điều hành | Mặc dù ứng dụng này hiện đã tồn tại |
| `generic` | không có | không có | none: **tự chứng thực** | – |

Sử dụng một dự án, nhóm, tài khoản hoặc tài khoản con dành riêng cho từng vụ việc: quyền truy cập chỉ đọc của người xác minh sau đó sẽ chỉ hiển thị triển khai này. Thông tin đăng nhập được đọc từ `--provider-token-file` hoặc biến ở trên, không bao giờ từ dòng lệnh. Đối với AWS, tệp chứa `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; khu vực là `--location`.

Những thông tin mà bản ghi của từng nhà cung cấp không thể hiển thị sẽ được in trong mỗi báo cáo. Tóm lại: Hetzner ghi lại các yêu cầu trên bảng điều khiển; Bảng điều khiển Khôi phục của DigitalOcean, Lish/Glish của Linode và bảng điều khiển web của Vultr không được ghi lại theo cách này, do đó quyền root bị khóa ngay từ lần khởi động đầu tiên và việc đăng nhập vào bảng điều khiển sẽ yêu cầu đặt lại mật khẩu hoặc thay đổi chế độ khởi động, những thao tác này đều được ghi lại. Vultr trả về địa chỉ bảng điều khiển cho bất kỳ khóa nào có thể truy cập vào instance; cả bản ghi lẫn báo cáo đều không lưu trữ thông tin này.

## Máy ảo bảo mật trên Phala Cloud (Intel TDX)

Với `--provider phala` trình thu thập chạy trong một máy ảo bảo mật Intel TDX trên [Phala Cloud](https://phala.com/), được quản lý bởi dstack. Máy chủ và nhân viên của Phala không thể đọc bộ nhớ của nó, và bộ xử lý ký xác nhận về những gì máy đã khởi động. Trình xác minh không chỉ tin vào lời của Phala: `tgwitness.tdx` mà tự kiểm tra từng bản xác nhận, lên đến Intel SGX Root CA được ghim, so sánh với danh sách thu hồi của Intel và dữ liệu nền tảng được ký bởi Intel, đồng thời từ chối các máy có thể bị gỡ lỗi hoặc di chuyển.

| Nhập báo cáo | Nội dung hiển thị |
| --- | --- |
| `tdx_binding` | Giấy chứng nhận bao gồm tuyên bố đã được ký của người thu thập và giá trị ngẫu nhiên của yêu cầu này |
| `tdx_quote` | Intel xác nhận tính hợp lệ của chứng nhận; chứng nhận chỉ được cấp khi Intel đánh giá nền tảng đó là cập nhật nhất |
| `tdx_compose_hash` | RTMR3, được tái tạo từ nhật ký sự kiện dstack, đo lường quá trình soạn thảo trong ứng dụng mà trình thu thập dữ liệu báo cáo |
| `tdx_compose` | Mã nguồn đó, từng byte một, chính là mã nguồn được xây dựng từ commit đã triển khai: các tệp nguồn được cố định bằng băm, cả hai hình ảnh đều được cố định bằng bản tóm tắt, không có mã nguồn nào khác |
| `tdx_identity` | Chứng nhận này được tạo ra từ ứng dụng và phiên bản đã triển khai, sử dụng các khóa từ hệ thống quản lý khóa (KMS) của Phala và một đĩa được mã hóa |
| `tdx_os` | Với `--tdx-measurements`, MRTD và RTMR0-2 bằng các giá trị được tính toán từ hình ảnh hệ điều hành dstack (`dstack-mr measure --json`) |

Mỗi lần khởi động trình thu thập được ghi lại trong nhật ký đều kèm theo chứng nhận như vậy, do đó `verify --evidence` kiểm tra mỗi lần khởi động. Danh sách các bản sửa đổi ứng dụng của Phala đóng vai trò là nhật ký nhà cung cấp: nếu nội dung soạn thảo thay đổi sau khi triển khai, báo cáo sẽ không thành công.

Trong bảng điều khiển, chọn **Máy ảo bảo mật · Phala Cloud** trong **mục Extras** → **Server 24/7** và dán khóa API Phala Cloud; đường hầm nhanh hoạt động tương tự như trên Hetzner. Từ dòng lệnh:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --tdx-measurements dstack-mr.json
```

`--tdx-collateral` đọc các chứng chỉ và danh sách thu hồi của Intel từ một tệp thay vì tải chúng xuống từ Intel. Dịch vụ Gateway DNS không khả dụng tại đây: Phala không có tường lửa của nhà cung cấp cho lưu lượng truy cập đi.

Một chứng nhận không thể loại trừ lỗ hổng trong mô-đun TDX hoặc vi mã của Intel, hoặc quyền truy cập vật lý vào bus bộ nhớ. Bất kỳ ai kiểm soát ứng dụng trong tài khoản của Phala đều có thể triển khai một bản soạn thảo khác; nó sẽ xuất hiện dưới dạng một bản sửa đổi mới với mã băm soạn thảo mới. Máy chủ kiểm soát nguồn thời gian và mạng của máy.

## Trước khi bắt đầu

1. Một vùng Cloudflare, ID tài khoản của vùng đó và một mã thông báo API có quyền **Cloudflare Tunnel Edit**, **Zone Read** và **DNS Edit**, được cung cấp cùng với `--cloudflare-token-file` hoặc `CLOUDFLARE_API_TOKEN`. Đối với người xác minh: **Cloudflare Tunnel Read**, **DNS Read** và, đối với nhật ký kiểm toán, **Account Settings Read**. Nếu không có tên miền, một [đường hầm nhanh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/#quick-tunnel-without-a-domain) không cần bất kỳ thông tin nào trong số này.
2. Thông tin đăng nhập của nhà cung cấp có quyền ghi vào một dự án chuyên dụng; `lock` cũng sử dụng cùng một:

   - Hetzner: Mã thông báo API có quyền Đọc & Ghi;
   - DigitalOcean: mã thông báo truy cập cá nhân có quyền ghi;
   - Linode: mã thông báo truy cập cá nhân với `linodes`, `firewall` và `events` phạm vi đọc/ghi;
   - Vultr: Khóa API của một tài khoản chuyên dụng hoặc tài khoản phụ;
   - AWS: Cho phép thông tin đăng nhập IAM `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` và `ec2:RevokeSecurityGroupIngress`.
3. Commit cần chạy. Một thẻ phát hành sẽ được giải quyết một lần duy nhất thành commit tương ứng với `git ls-remote`; máy chủ chỉ nhận được commit dài 40 ký tự.

## Từ bảng điều khiển

Trên máy tính của bạn, **Extras → Server 24/7** sẽ chạy dịch vụ tương tự `deploy` cho Hetzner chỉ trong ba bước: chọn Châu Âu hoặc Hoa Kỳ, dán mã thông báo Hetzner (Đọc & Ghi), sau đó xem lại loại máy chủ, giá hàng tháng, địa chỉ và phiên bản mà bảng điều khiển tìm thấy với mã thông báo đó. Không có gì được tạo ra trước khi bạn xác nhận. Bảng điều khiển hiển thị từng bước dưới dạng `deploy` báo cáo, sau đó là địa chỉ, mã thông báo của bảng điều khiển và dấu vân tay khóa ký. Nếu không có tên miền, máy chủ sẽ được cấp một [đường hầm nhanh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; **mục Máy chủ của bạn → Tìm địa chỉ hiện tại** sẽ tra cứu lại sau khi khởi động lại. Để có địa chỉ cố định dưới tên miền của riêng bạn, hãy mở **Tùy chọn · tên miền của riêng bạn** và thêm mã thông báo Cloudflare (liên kết đã chuẩn bị sẽ chọn Zone Read, DNS Edit và Cloudflare Tunnel Edit).

Các mã thông báo được truyền cùng với mỗi yêu cầu từ tab trình duyệt đến TgWitness trên cùng một máy tính và không được lưu ở bất kỳ đâu; bản ghi triển khai, cloud-init đã được che giấu, mã thông báo bảng điều khiển và, đối với đường hầm nhanh, khóa địa chỉ được lưu trữ trong `deployments/NAME` bên trong thư mục dữ liệu. Bảng điều khiển chỉ cung cấp tính năng này cho quản trị viên chính qua kết nối loopback trực tiếp (`127.0.0.1`, không có tiêu đề proxy hoặc đường hầm); một bảng điều khiển được truy cập qua mạng sẽ hiển thị các lệnh thay vào đó. Phiên bản mặc định là thẻ phát hành của bảng điều khiển đang chạy, được xác định thông qua API GitHub. Vị trí, loại máy chủ và giá cả lấy từ API của Hetzner: `cpx22` nếu dịch vụ này được cung cấp tại đó, nếu không thì sẽ là loại x86 rẻ nhất với ít nhất 2 GB bộ nhớ.

## Tunnel nhanh mà không cần tên miền

`--quick-tunnel` thay thế `--zone`, `--cloudflare-account` và `--panel-host`; không liên quan đến tài khoản hoặc mã thông báo Cloudflare:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

Trên máy chủ, cloudflared mở một [đường hầm nhanh](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) đến bảng điều khiển: một địa chỉ ngẫu nhiên `https://….trycloudflare.com` thay đổi mỗi khi cloudflared hoặc máy chủ khởi động lại. Một dịch vụ nhỏ trên máy chủ đăng mỗi địa chỉ lên một chủ đề ngẫu nhiên trên ntfy.sh , được ký (HMAC-SHA256) bằng một khóa chỉ có trong thư mục triển khai (`address-key.txt`), và lặp lại việc này cứ sau ba giờ vì ntfy.sh lưu giữ các bài đăng trong 12. `deploy` và **Tìm địa chỉ hiện tại** chỉ chấp nhận các bài đăng được ký, do đó một bài đăng giả mạo không thể chuyển bạn và mã thông báo bảng điều khiển của bạn đến địa chỉ của người khác. Chủ đề này được lưu trong bản ghi và cloud-init đã được công bố: bất kỳ ai có chúng đều có thể đọc địa chỉ hiện tại, địa chỉ này vẫn yêu cầu mã thông báo bảng điều khiển. Máy chủ không giữ bất kỳ cổng vào nào trong cả hai trường hợp.

Chi phí: không có tài khoản Cloudflare nào lưu trữ bản ghi về đường hầm tạm thời, do đó `verify` báo cáo rằng kênh, bộ kết nối và kiểm tra DNS không khả dụng và kết quả tốt nhất là `incomplete`; các bản ghi của nhà cung cấp, tường lửa, tuyên bố đã ký, đo lường máy chủ và so sánh trình cài đặt được kiểm tra như bình thường. Việc so sánh byte với trình cài đặt tham chiếu cần một bản commit đã triển khai đã biết trước `--quick-tunnel`; một bản checkout 0.7.0 sẽ xây dựng trình cài đặt miền và báo cáo sự khác biệt. Cloudflare không đảm bảo thời gian hoạt động cho các đường hầm nhanh, cho phép 200 yêu cầu đang được xử lý và không hỗ trợ Server-Sent Events, do đó các cập nhật trực tiếp trên bảng điều khiển (các phiên bản sau 0.7.0) có thể không được truyền qua đường hầm này và cần tải lại trang; phần này chưa được thử nghiệm. Đối với trường hợp cần đảm bảo tính ổn định, hãy sử dụng tên miền của riêng bạn.

## Triển khai

Hãy xem trước tất cả những gì sẽ được gửi đi. `plan` không thực hiện bất kỳ yêu cầu nào đến nhà cung cấp hoặc Cloudflare:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Sau đó, triển khai với các tùy chọn và thông tin đăng nhập tương tự:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Các loại máy chủ để bắt đầu: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` và `--image` mặc định là Ubuntu 24.04 của từng nhà cung cấp tại khu vực châu Âu.

`--repository` lấy bản cam kết từ một kho lưu trữ Git https khác, mà không cần thông tin đăng nhập trong URL (mặc định `https://github.com/phishdestroy/TgWitness.git`). `deploy` cũng chấp nhận `--out` cho một thư mục triển khai khác (mặc định `deployments/NAME`; một thư mục đã chứa sẵn một triển khai sẽ bị từ chối) và `--wait`, số phút chờ bản tuyên bố đã ký của trình thu thập: từ 1 đến 240, mặc định là 20, hoặc 60 cho `generic`.

Lệnh:

1. tạo một đường hầm Cloudflare, trong đó lưu lượng truy cập vào (ingress) chuyển tiếp tên miền máy chủ của bảng điều khiển đến bảng điều khiển và, nếu có, tên miền máy chủ của witness đến `/api/witness/head` và `/api/assurance` chỉ;
2. tạo các bản ghi CNAME được chuyển tiếp cho các tên máy chủ đó, từ chối các tên đã tồn tại;
3. tạo một tường lửa nhà cung cấp không có quy tắc vào và một máy chủ phía sau nó không có khóa SSH, không có bản sao lưu, không có tác nhân console, và cloud-init che giấu SSH, khóa quyền root, cài đặt `cloudflared`, tải chính xác bản cam kết, kiểm tra nó và khởi động TgWitness dưới dạng dịch vụ systemd được tăng cường bảo mật;
4. chờ nhận bản tuyên bố đã được ký bởi trình thu thập và kiểm tra xem bản tuyên bố đó có đề cập đến máy chủ này và băm của tệp cloud-init này hay không.

`deployments/case-2026-11/` sau đó chứa:

| Tệp | Nội dung | Chia sẻ? |
| --- | --- | --- |
| `deployment.json` | ID, băm, các lệnh gọi API đã thực hiện (phương thức, đường dẫn, trạng thái) và tuyên bố được ký đầu tiên | Có, với trình xác minh |
| `cloud-init.redacted.yaml` | Câu lệnh cloud-init chính xác với hai khóa bí mật được thay thế bằng `REDACTED` | Có |
| `panel-token.txt` | Mã thông báo bảng điều khiển | Không |

Mật khẩu root của nhà cung cấp, mã thông báo đường hầm và mã thông báo bảng điều khiển không bao giờ được ghi vào `deployment.json`. Hãy công bố dấu vân tay của bộ thu thập được hiển thị ở phần cuối thông qua một kênh mà bạn không kiểm soát một mình, ví dụ như một kênh chứng kiến hoặc một tin nhắn gửi đến người nhận.

Đăng nhập vào Telegram tại `https://case.example.org` với mã thông báo bảng điều khiển, như được hướng dẫn trong [hướng dẫn tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/). Các hành động trên bảng điều khiển được ghi lại trong nhật ký đã được ký; chúng không phải là các phiên SSH. Một [nhân chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/) có thể kiểm tra `https://case-witness.example.org`.

Không có SSH: nếu quá trình khởi động thất bại, trình thu thập dữ liệu sẽ không bao giờ phản hồi. Hãy xóa máy chủ và triển khai lại, hoặc sử dụng triển khai gỡ lỗi để tìm nguyên nhân.

### Thông tin bí mật trong dữ liệu người dùng

Cloud-init chứa hai thông tin bí mật: mã thông báo bảng điều khiển và mã thông báo đường hầm Cloudflare. Khóa ký không nằm trong số đó; nó được tạo trên máy chủ. Hetzner, DigitalOcean và Linode không trả về dữ liệu người dùng qua API của họ. Vultr trả về dữ liệu cho bất kỳ khóa nào có thể đọc phân vùng, và EC2 thông qua `DescribeInstanceAttribute`. Đối với AWS, chỉ cung cấp cho người xác minh ba hành động trong bảng, tuyệt đối không `ec2:Describe*`. Đối với Vultr, giả định rằng khóa của người xác minh có thể đọc cả hai mã thông báo. Mã thông báo đường hầm cho phép ai đó chạy một trình kết nối thứ hai: `verify` báo cáo bất kỳ trình kết nối nào không có trên máy chủ, và các tuyên bố của bộ thu thập không thể bị làm giả theo cách đó vì mỗi tuyên bố đều ký một thách thức mới. Với `--quick-tunnel` mật khẩu thứ hai là khóa địa chỉ thay vào đó: bất kỳ ai đọc được nó đều có thể đăng một địa chỉ giả mà bảng điều khiển sẽ chấp nhận.

Tuyên bố công khai của người thu thập dữ liệu không đề cập đến địa chỉ máy chủ và nguồn đăng nhập; cả hai thông tin này đều được lưu giữ trong nhật ký đã được ký xác thực.

## Gỡ lỗi triển khai và khóa

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` giữ SSH cho một khóa từ một địa chỉ hoặc mạng nhỏ, tối đa là /24 đối với IPv4 hoặc /48 đối với IPv6. `KEY` đã được đăng ký với nhà cung cấp: tên hoặc ID của một khóa SSH trong dự án Hetzner, ID hoặc dấu vân tay của một khóa SSH trong nhóm DigitalOcean, tên người dùng Linode có các khóa SSH trong hồ sơ được thêm vào tài khoản root, ID của một khóa SSH trong tài khoản Vultr, hoặc tên của cặp khóa EC2 trong khu vực. Các tùy chọn này không áp dụng cho `generic`. Việc triển khai như vậy được ghi nhận là `debug` và **không bao giờ** được báo cáo là có độ bảo mật cao. Khi hoàn tất, hãy chạy `sudo tgwitness-lock` làm lệnh cuối cùng của phiên SSH cuối cùng, sau đó:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

Tường lửa mất tất cả các quy tắc kết nối vào. Các báo cáo sau đó hiển thị thời điểm SSH được phép và thời điểm nó bị đóng; cửa sổ đó vẫn hiển thị.

## Xóa một bản triển khai

`destroy` xóa máy chủ và tường lửa của nó, được xác định bằng nhãn của bản triển khai để đảm bảo rằng một bản triển khai bị lỗi giữa chừng cũng sẽ bị xóa, sau đó là các bản ghi DNS trỏ đến đường hầm của nó, và chính đường hầm đó. Nhật ký máy chủ và khóa ký cũng bị xóa cùng lúc: hãy xuất bằng chứng trước. Bản ghi vẫn được lưu lại, được đánh dấu `removed`, cùng với các lệnh gọi API của quá trình xóa.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Việc xóa qua API đã được triển khai cho Hetzner. Đối với các nhà cung cấp khác `destroy` phải dừng lại trước khi xóa bất kỳ thứ gì và chỉ định nhãn cần xóa trong bảng điều khiển của nhà cung cấp. Một máy chủ được cài đặt thủ công (`generic`) chỉ mất đường hầm và bản ghi DNS của nó. Việc triển khai đường hầm nhanh không cần mã thông báo Cloudflare: đường hầm của nó kết thúc tại máy chủ, và các bài đăng của nó sẽ hết hạn trên ntfy.sh trong vòng 12 giờ.

## Bất kỳ máy chủ nào (được tự chứng thực)

`--provider generic` dành cho máy chủ được mua hoặc cài đặt thủ công. `deploy` tạo đường hầm và DNS, ghi `install.sh` (riêng tư) và `install.redacted.sh` (để công khai), và chờ đợi. Sao chép `install.sh` vào một máy chủ Ubuntu 24.04 vừa cài đặt xong và chạy nó tại đó:

```
sudo bash install.sh
```

Nó ghi lại máy chủ ở trạng thái ban đầu (thông tin đăng nhập, tài khoản, `authorized_keys`, các socket lắng nghe, dịch vụ, tác vụ được lên lịch, gói phần mềm), cài đặt bản cam kết, kích hoạt tường lửa máy chủ, tự xóa bản thân, ẩn địa chỉ SSH và kết thúc phiên làm việc. Báo cáo cho một máy chủ như vậy tốt nhất chỉ là **TỰ CHỨNG NHẬN**: bất kỳ ai chạy trình cài đặt đều đã có quyền root trước đó, và không có bản ghi nào từ nhà cung cấp có sẵn cho người xác minh. Tuy nhiên, điều này vẫn tốt hơn so với một máy chủ không rõ nguồn gốc: danh sách tài sản, băm của trình cài đặt và mọi lần đăng nhập sau đó đều được ký điện tử.

## Xác minh

Người xác minh cần `deployment.json`, trình cài đặt đã được công bố, thông tin đăng nhập chỉ đọc và, tốt nhất là bản checkout của commit và bằng chứng ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Mọi giá trị từ nhà cung cấp và Cloudflare đều được trình xác minh yêu cầu tại thời điểm đó; bản ghi chỉ cung cấp các ID cần tra cứu. Mã thoát là 0 cho **PASS**, 1 cho **FAIL** và 2 cho **REVIEW**, **INCOMPLETE** hoặc **SELF-ATTESTED**. `--fingerprint` phải đến từ một kênh độc lập ; nếu không có nó, khóa sẽ chỉ được so sánh với bản ghi của nhà điều hành. `python verify.py` vẫn tự xác minh bằng chứng ZIP, như trong [phần Bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/).

Các hành động của nhà cung cấp được phân loại: tạo mới và khởi động trong vòng 30 phút kể từ khi tạo sẽ được chấp nhận; các hành động liên quan đến console, cứu hộ, đặt lại mật khẩu, xây dựng lại, ISO, hình ảnh, ảnh chụp nhanh, sao lưu, Systems Manager, kết nối EC2 Instance và mở cổng tường lửa sẽ bị từ chối; các hành động liên quan đến nguồn điện và bất kỳ hành động nào không mong đợi sẽ được đánh dấu để xem xét. Một hành động không xác định sẽ không bao giờ được chấp nhận mà không có cảnh báo.

## Báo cáo về việc bàn giao bằng chứng

`--report report.md` viết báo cáo Markdown và `report.json` bên cạnh đó:

1. kết quả, dấu vân tay khóa thu thập, triển khai, nhà cung cấp, cam kết, máy chủ, tường lửa, đường hầm;
2. mỗi lần kiểm tra kèm theo trạng thái và nguồn (API của nhà cung cấp, API Cloudflare, báo cáo của bộ thu thập, sổ ghi chép bằng chứng);
3. nhật ký của nhà cung cấp với đánh giá về mỗi hành động và, nếu nhà cung cấp ghi lại, thì cả thông tin về chủ thể thực hiện hành động đó;
4. các điểm cuối Cloudflare lưu trữ các kết nối, cấu hình và nhật ký kiểm toán của đường hầm;
5. bản tuyên bố đã được ký của người thu thập;
6. những gì báo cáo xác định và những gì báo cáo không xác định;
7. các lệnh để tái tạo nó, và thẻ SHA-256 của mọi tệp được cung cấp.

Giao nộp báo cáo, `report.json`, `deployment.json`, trình cài đặt đã được phát hành và bằng chứng ZIP. Hãy lập báo cáo sớm: nhật ký của nhà cung cấp chỉ được lưu giữ trong một khoảng thời gian giới hạn.

## Cloudflare với vai trò là bên chứng kiến bên ngoài

Mọi thứ ở đây đều là tùy chọn. Ngay cả khi không có tài khoản Cloudflare, máy chủ vẫn hoạt động, và hai trong số các tùy chọn này hiện đang hoạt động:

| Nội dung | Nội dung hiển thị | Trong TgWitness |
| --- | --- | --- |
| Tunnel nhanh hoặc tunnel của tên miền của bạn | Bảng điều khiển chỉ có thể truy cập thông qua đường hầm | trình hướng dẫn cài đặt máy chủ, xem ở trên |
| drand relay `drand.cloudflare.com` | các bản ghi sau vòng drand mới hơn bản ghi này: nhật ký được viết theo tiến trình thực hiện | chế độ bằng chứng, **Thêm nhân chứng**, không có tài khoản ([định dạng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Thông báo về tình trạng đường hầm | khi đường hầm bị ngắt kết nối, qua email hoặc webhook từ Cloudflare | thiết lập chúng trong bảng điều khiển Cloudflare |
| Gateway DNS (`--gateway-dns`, hoặc **Cloudflare Gateway DNS** trong trình hướng dẫn) | mọi tên miền mà máy chủ đã tra cứu, được Cloudflare trả lời qua TLS; tường lửa Hetzner không cho phép DNS truy cập bất kỳ dịch vụ nào khác; liệu chính sách Gateway có thể sửa đổi các phản hồi hay không | Hetzner, gói Zero Trust miễn phí, không cần tên miền; `verify` kiểm tra tường lửa, vị trí, ghi nhật ký, chính sách, các truy vấn của máy chủ và nhật ký kiểm toán; chế độ bằng chứng sao chép nhật ký vào sổ nhật ký |
| Cổng kết nối với Cloudflare: Một client trên máy chủ, một tường lửa ra ngoài chỉ cho phép kết nối qua Cloudflare | mọi kết nối mà máy chủ thực hiện, không chỉ giới hạn ở DNS | chưa được xây dựng |
| Truy cập ở phía trước bảng điều khiển | Ai đã đăng nhập vào bảng điều khiển và vào thời điểm nào | chưa được triển khai: cần có tên miền riêng của bạn |
| Ghi nhật ký lệnh SSH | mỗi lệnh trong một phiên gỡ lỗi | chưa được xây dựng |

Logpush, tính năng giúp lưu giữ bản sao riêng của Cloudflare trong R2, là một tính năng dành cho doanh nghiệp: trên gói miễn phí , Cloudflare trả lời `logpush is not enabled for this account`. Nhật ký Gateway của nó tồn tại trong 24 giờ tại đó, do đó chế độ bằng chứng sẽ sao chép nó vào nhật ký đã ký (**nhật ký của Cloudflare Gateway về các truy vấn DNS của máy chủ này**, một token chỉ đọc với quyền Account Analytics Read).

Nếu không có kế hoạch Zero Trust, một tài khoản sẽ có một vị trí DNS. Khi Cloudflare từ chối một vị trí khác, máy chủ sẽ chia sẻ vị trí hiện có và các truy vấn của nó được phân biệt thông qua địa chỉ; bộ lọc đó cũng cần quyền truy cập Zero Trust PII Read, và `destroy` để lại một vị trí được chia sẻ. Một truy vấn nhật ký kéo dài tối đa ba giờ, do đó việc sao chép và `verify` đọc dữ liệu theo các khung thời gian ba giờ trong ngày.

Gateway DNS bao gồm bộ giải quyết tên miền của hệ thống. DNS qua HTTPS trên cổng 443 đến một bộ giải quyết tên miền khác, và các kết nối đến một địa chỉ không được tra cứu ở bất kỳ đâu (ví dụ như các trung tâm dữ liệu của Telegram) sẽ không được ghi lại trong nhật ký của nó.

Cloudflare không thể xem nội dung bên trong lớp mã hóa của Telegram, các thiết bị khác trên tài khoản Telegram (danh sách thiết bị trong chế độ bằng chứng ghi lại chúng từ phía Telegram) hoặc hypervisor của nhà cung cấp.

## Điều này không xác định được

- Nhà cung cấp và nhân viên của họ quản lý hypervisor, đĩa cứng và mạng.
- Các chỉ số máy chủ được báo cáo tự động bởi trình thu thập dữ liệu.
- Nội dung các quy tắc tường lửa trước đây không có trong nhật ký của mọi nhà cung cấp; chỉ có Linode lưu giữ các phiên bản quy tắc.
- Nó không đề cập đến bất kỳ thông tin mới nào về tính xác thực của tin nhắn; xem phần [Bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/).

Chưa được chạy trên các tài khoản thực: một bản triển khai dưới tên miền riêng của bạn (đường hầm Cloudflare và DNS), các nhà cung cấp khác, một bản triển khai gỡ lỗi và `lock`, một tài khoản Telegram trên máy chủ đó, và các bản cập nhật trực tiếp của các phiên bản sau thông qua đường hầm nhanh. Kiểm tra lần triển khai đầu tiên trên mỗi nhà cung cấp với `plan`, một triển khai gỡ lỗi và `verify` trước khi sử dụng nó trong một vụ việc.
