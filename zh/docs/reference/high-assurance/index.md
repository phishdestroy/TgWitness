# 高可信度部署

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/

部署在 Hetzner 或 Phala Cloud 上的全天候密封服务器、网关 DNS 以及第三方可复现的验证机制。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文档](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/zh/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

High-assurance deployment adds independent checks of the collection environment to archive verification. The reviewer queries deployment and access records held by the cloud provider and Cloudflare, and an Intel TDX deployment adds hardware attestation of the collector's environment.

常规的本地和 Docker 使用方式保持不变。除非您使用 `python -m tgwitness.cloud`进行部署，且收集器仅在部署设置为 `TGWITNESS_ASSURANCE`.

流程图 · 操作员 → 服务器，防火墙未配置入站规则 (提供商 API); 操作员 → 隧道与 DNS (Cloudflare API); 服务器，防火墙未配置入站规则 → 隧道与 DNS (仅限外发); 服务器，防火墙未配置入站规则 → 在服务器上生成的签名密钥; Verifier，只读令牌 → 提供商日志和防火墙; Verifier，只读令牌 → 隧道连接器地址和入口; Verifier，只读令牌 → 已签名的 /api/assurance 声明; Verifier，只读令牌 → 证据 ZIP · 操作员 · Verifier，只读令牌 · 服务器，防火墙未配置入站规则 · 提供商日志和防火墙 · 隧道连接器地址和入口 · 已签名的 /api/assurance声明 · 证据 ZIP · 隧道与 DNS · 在服务器上生成的签名密钥 · 提供商 API · Cloudflare API · 仅限外发

**图表转为文本**

1. 操作员 → 服务器，防火墙未配置入站规则 (提供商 API)
2. 操作员 → 隧道与 DNS (Cloudflare API)
3. 服务器，防火墙未配置入站规则 → 隧道与 DNS (仅限外发)
4. 服务器，防火墙未配置入站规则 → 在服务器上生成的签名密钥
5. Verifier，只读令牌 → 提供商日志和防火墙
6. Verifier，只读令牌 → 隧道连接器地址和入口
7. Verifier，只读令牌 → 已签名的 /api/assurance 声明
8. Verifier，只读令牌 → 证据 ZIP

**On this page**

- [What a verifier can check](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#what-a-verifier-can-check)
- [Providers](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#providers)
- [Confidential VM on Phala Cloud (Intel TDX)](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [Before you start](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#before-you-start)
- [From the panel](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#from-the-panel)
- [Quick tunnel without a domain](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [Deploy](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#deploy)
- [Debug deployment and lock](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#debug-deployment-and-lock)
- [Remove a deployment](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#remove-a-deployment)
- [Any server (self-attested)](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#any-server-self-attested)
- [Verify](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#verify)
- [Report for evidence handover](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#report-for-evidence-handover)
- [Cloudflare as an outside witness](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [Reading the deployment result](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#reading-the-deployment-result)

## 验证者可以检查的内容

| 声明 | 如何进行验证 | 维护者： |
| --- | --- | --- |
| 该服务器是在已知时间点通过服务商 API 创建的 | 服务器对象及其在提供商自有日志中的创建过程 | 提供商 |
| 没有人使用该提供商的访问路径 | 控制台请求、救援、密码重置、重建、ISO、镜像和备份的日志 | 提供商 |
| 无法连接到它 | 提供商防火墙没有入站规则；SSH 服务在首次启动时即被屏蔽 | 提供商（防火墙）、主机（SSH） |
| 该面板仅可通过隧道访问 | 隧道入口仅将流量转发至控制面板；连接器从服务器地址运行 | Cloudflare |
| 该软件的运行情况如下： | 收集器的签名源代码树哈希值与已部署提交的检出结果相等 | Collector，已与 Git 进行过校验 |
| 该签名密钥是在该服务器上生成的 | 该密钥会签署一份声明，其中包含服务提供商的服务器 ID 以及收到的 cloud-init 的哈希值 | Collector，已与提供商进行过核对 |
| 该日志属于该密钥和服务器 | 证据ZIP中的每个进程启动时，都会携带该服务器的宿主测量数据 | 证据 ZIP |

The collector records SSH state, sessions, login history and boot information in signed process-start and `host.state` records. On an ordinary VM these are local inventory records, which the reviewer compares with the provider's independent records. The Intel TDX deployment below additionally verifies hardware-backed measurements.

## 提供商

| `--provider` | 凭据 | 验证员的只读访问权限 | 验证器的提供者日志 | 保留用于 |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | 同一项目的读取令牌 | 服务器和防火墙操作 | 只要这些资源存在 |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | 只读个人访问令牌 | Droplet 操作 | 只要 Droplet 存在 |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` 只读范围 | 账户事件、防火墙规则版本 | 90 天 |
| `vultr` | `VULTR_API_KEY` | 具有读取权限且拥有 `activity_logs` 权限 | 账户活动日志（方法、路径、操作者） | 30 天，订阅审计日志可延长保存期限 |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrail 事件历史记录 | 90 天 |
| `phala` | `PHALA_CLOUD_API_KEY` | 同一工作区的 API 密钥 | 应用程序修订与 CVM 操作：Docker Compose 配置和环境变更、重启、操作系统升级 | 虽然该应用程序已存在 |
| `generic` | 无 | 无 | 无：**自我认证** | – |

请为每个案例使用专用的项目、团队、账户或子账户：这样，验证者的 只读访问权限将仅显示此部署。凭据从 `--provider-token-file` 或上述变量中读取，绝不从命令行获取。对于 AWS，该文件 包含 `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`；区域为 `--location`.

每份报告中都会注明各服务商记录中无法显示的内容。 简而言之：Hetzner 会记录控制台请求；而 DigitalOcean 的恢复控制台、Linode 的 Lish/Glish 以及 Vultr 的 Web 控制台则不会被直接记录，因此 root 账户在首次启动时会被锁定，若要登录控制台 则需要重置密码或更改启动方式，而这些操作会被记录下来。Vultr 会向任何能够读取该实例的密钥返回控制台 地址；但记录和报告中均不会存储该地址。

## Phala Cloud 上的机密虚拟机（Intel TDX）

该 `--provider phala` 收集器运行在 [Phala Cloud](https://phala.com/) 上的英特尔 TDX 机密虚拟机中， 由 dstack 管理。主机和 Phala 工作人员无法读取其 内存，且处理器会对机器的启动过程生成一份认证声明并进行签名。验证器不会 仅凭 Phala 的声明就予以采信： `tgwitness.tdx` 会自行核查每份证明——直至固定的英特尔 SGX 根证书颁发机构（Root CA）——并将其与英特尔的撤销列表及英特尔签名的平台数据进行比对，同时拒绝 任何可被调试或迁移的机器。

| 报告条目 | 功能展示 |
| --- | --- |
| `tdx_binding` | 该证明涵盖了收集者的签名声明以及本次请求的随机值。 |
| `tdx_quote` | 英特尔对该认证负责；只有当英特尔将该平台评定为“最新”时，该认证才算通过。 |
| `tdx_compose_hash` | RTMR3 通过重放 dstack 事件日志，对收集器报告的 app-compose 进行测量 |
| `tdx_compose` | 该代码与已部署提交生成的代码字节对字节完全一致：源文件通过哈希值固定，两张图片均通过摘要固定，不存在其他代码 |
| `tdx_identity` | 该证明来自已部署的应用程序和实例，使用 Phala 的 KMS 提供的密钥以及加密磁盘。 |
| `tdx_os` | MRTD 和 RTMR0-2 的值等于验证器根据 Dstack-TEE 发布的 dstack 操作系统镜像计算得出的值，该值通过 CVM 报告的操作系统镜像哈希以及 QEMU 根据虚拟机配置生成的 ACPI 表确定：固件、内核、initrd、包含根文件系统哈希的命令行、内存、vCPU 和设备。开发镜像将导致验证失败 |

操作系统镜像（约 180 MB，其中保留 21 MB）从 [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) 下载一次至 记录旁边的 `dstack-images`；`--tdx-image FOLDER` 使用另一个文件夹或解压后的镜像， `--tdx-image none` 跳过比较步骤。 测量过程遵循 `dstack-mr` 以及来自 Dstack-TEE/dstack 的 `qemu-acpi` Rust 包；`tools/check_dstack_image.py` 将其与 QEMU 自身的 ACPI 输出以及真实的 Phala Cloud 硬件认证记录进行比对，`--live` 还将其与已发布的镜像进行比对。 `--tdx-measurements` 仍会比较以 JSON 格式提供的 MRTD 和 RTMR0-2。

日志中记录的每次收集器启动都附有此类证明，因此 `verify --evidence` 会检查每次启动及其引导的操作系统镜像。Phala 的应用程序修订版本 和 CVM 的操作充当提供商日志：部署后 Docker Compose 配置的任何更改 都会导致报告失败，且重启记录将被列出以供审查。

在面板中，选择**“附加功能** → **7×24小时服务器** ”下的**“机密虚拟机 · Phala Cloud** ”，并粘贴 Phala Cloud API 密钥；快速隧道的工作原理与 Hetzner 上相同。在命令行中：

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` 从文件中读取英特尔的证书和撤销列表，而不是 从英特尔下载。此处无法使用网关 DNS：Phala 没有用于 出站流量的提供商防火墙。

### 认证证书

对于 Phala 部署，`verify --report certificate.md` 还会写入证书：一个 自包含的 `certificate.html` 文件和一份 A4 规格的 `certificate.pdf` 文件，其中包含验证结果、从英特尔根证书到收集器密钥的信任链、 与普通服务器及高保障服务器的对比分析、 与基于已发布镜像计算出的数值并列的测量结果、各部分的担保方、 英特尔证书链、每项检查、提供商日志，以及如何重复进行 验证。 JSON 报告仍是权威记录；这些页面仅用于呈现其内容。

该报告已通过签名和时间戳进行数字封存，封存文件为 `certificate.seal.json` 及其旁边的 `.tsq`/`.tsr` 文件：

| Seal | 新增功能 |
| --- | --- |
| 合格电子时间戳，`http://tsa.belgium.be/connect` | RFC 3161 时间戳基于比利时联邦政府合格信任服务提供商（FPS 政策与支持局，BOSA）提供的 `certificate.json` 的精确字节数据。 该机构被列入比利时欧盟可信列表，状态为“已授予”，属于合格时间戳服务；截至 2026 年 10 月 20 日发布的列表，其根证书（比利时根 CA6）及列表条目均被固定在 `tgwitness/tsa_roots.py` 中。 根据《欧盟法规》第 910/2014 号第 41 条，此类时间戳在所有欧盟成员国中，其日期、时间以及数据完整性均被推定为准确。 |
| RFC 3161 时间戳，FreeTSA | 第二个独立的时间戳 |
| 验证器签名 | Ed25519 基于一条声明对报告的 SHA-256 值和每个时间戳进行签名，使用验证者自身的密钥（`--sign-with FOLDER`，默认 `~/.tgwitness/verifier`）；PDF 文件带有由同一密钥生成的签名 |

`--timestamp URL`（可重复）选择其他认证机构，`--timestamp none` 不选择任何机构，`--sign-with
none` 不对印章进行签名。`check-report` 会验证报告的哈希值、验证者签名、 每个时间戳与受信任根证书的关联及其合格状态，以及 PDF 文件的签名。 在欧盟以外地区， 合格时间戳以及报告整体的法律效力，由接收它的法院 或主管部门决定；该印章表明报告的生成时间以及其内容未被篡改。

一份认证报告无法排除英特尔 TDX 模块或微代码中存在漏洞，也无法排除对 内存总线的物理访问。无论谁控制了 Phala 账户中的应用程序，都可以部署另一个“compose”； 它将显示为一个带有新“compose”哈希值的新版本。主机控制着机器的 时间源和网络。

部署、使用 `--evidence` 进行验证、重启、操作系统镜像比较、带有签名和时间戳的数字密封证书以及 销毁操作均已在 Phala Cloud 平台上运行；参见 [（2026 年 11 月 4 日运行）和](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)。

## 开始之前

1. 一个 Cloudflare 区域、其账户 ID 以及一个具有 **Cloudflare Tunnel 编辑**、 **区域读取**和 **DNS 编辑权限的** API 令牌，由 `--cloudflare-token-file` 或 `CLOUDFLARE_API_TOKEN`。对于验证者：**Cloudflare Tunnel 读取**、**DNS 读取**，以及针对 审计日志的**账户设置读取**。若无域名， [快速隧道](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#quick-tunnel-without-a-domain)则无需上述任何信息。
2. 具有专用项目写入权限的提供商凭据； `lock` 同样使用：

   - Hetzner：具有读写权限的 API 令牌；
   - DigitalOcean：具有写入权限的个人访问令牌；
   - Linode：个人访问令牌，包含 `linodes`, `firewall` 和 `events` 读写权限；
   - Vultr：专用账户或子账户的 API 密钥；
   - AWS：允许使用 IAM 凭据 `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` 且 `ec2:RevokeSecurityGroupIngress`.
3. 待执行的提交。发布标签会通过以下方式解析为对应的提交： `git ls-remote`； 服务器仅接收该 40 个字符的提交信息。

## 来自面板

在您的电脑上，**通过“扩展功能”→“24/7 服务器”**即可为 Hetzner 运行相同的 `deploy` Hetzner服务，仅需三个 步骤：选择欧洲或美国，粘贴Hetzner令牌（读写权限），然后核对 控制面板根据该令牌检索到的服务器类型、月费、地址及版本。在您确认之前， 不会创建任何内容。控制面板会将每个步骤显示为 `deploy` 报告显示，随后显示 地址、面板令牌和签名密钥指纹。若未绑定域名，服务器将获得 [快速隧道](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ；重启后，**通过“您的服务器”→“查找当前地址** ”可再次查询。若要在自有域名下设置固定地址，请打开 **“可选”→“自有域名** ”，并添加 Cloudflare 令牌（预设链接会自动选择“区域 读取”、“DNS 编辑”和“Cloudflare 隧道编辑”）。

这些令牌随每次请求从浏览器标签页传输至同一台计算机上的 TgWitness， 且不会被写入任何位置；部署记录、经过处理的 cloud-init、面板令牌以及 用于快速隧道的地址密钥均保存在 `deployments/NAME` 数据目录内。 面板仅通过直接回环连接向主管理员提供此功能 （`127.0.0.1`，不允许代理或隧道头部）；通过网络访问的面板则会显示相关命令 。版本默认采用运行中面板的发布标签，该标签通过 GitHub API解析获得。位置、服务器类型和价格来自Hetzner的API： `cpx22` 在提供该服务的地方 使用该服务，否则使用内存至少为 2 GB 的最便宜 x86 类型。

## 无需域名的快速隧道

`--quick-tunnel` 替换 `--zone`, `--cloudflare-account` 并 `--panel-host`；无需使用 Cloudflare 账户或令牌：

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

在服务器端，cloudflared 会打开一条 [快速隧道](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) 连接到控制面板：一个随机的 `https://….trycloudflare.com` 地址，该地址会在 cloudflared 或服务器重启时发生变化。服务器上一个小型服务会将每个地址发布到一个随机的 ntfy.sh 主题中，并使用仅部署目录中保存的密钥进行签名（HMAC-SHA256） （`address-key.txt`），并每三小时重复一次，因为 ntfy.sh 会保留帖子 12. `deploy` 和**“查找当前地址”**功能仅接受签名帖子，因此伪造的帖子无法 将您和您的面板令牌重定向到他人的地址。该主题记录在 已发布的 cloud-init 中：任何拥有这些信息的人都能读取当前地址，而该地址仍会要求提供 面板令牌。无论哪种方式，服务器均不保留任何入站端口。

验证器没有地址密钥，任何读取该主题的人都可以向其发布消息。因此，收集器 还会发布该地址本身，并使用其自身的 Ed25519 密钥进行签名；`verify` 会取部署记录中 由收集器密钥签名的最新发布消息；发布消息的排序依据是 ntfy.sh 接收它们的时间，而非它们声称的时间。 在此变更之前的收集器不会对任何内容进行签名，而 `verify` 随后会取最新的一条发布内容，并在 `statement` 检查中声明这一点；伪造的发布内容 只能导致该检查失败，因为该地址仍必须使用收集器的密钥进行响应。

代价：由于没有 Cloudflare 账户记录快速隧道，因此 `verify` 会报告 隧道、连接器和 DNS 检查不可用，结果最好也只能是 `incomplete`（在 Phala Cloud 上，检查反而通过：连接器在被测的 Docker Compose 配置中运行）； 提供商记录、防火墙、签名声明、主机测量和安装程序比较均 按常规进行检查。与参考安装程序的字节比较需要一个已部署的提交 版本，该版本已知 `--quick-tunnel`；从 0.7.0 版本检出后构建域名安装程序并报告 差异。 Cloudflare 对快速隧道不提供正常运行时间保证，允许 200 个请求 在传输中，且不传输服务器发送事件（Server-Sent Events），因此控制面板的实时更新（0.7.0 之后的版本） 可能无法通过快速隧道到达，需要重新加载页面；这一部分尚未经过测试。对于 必须保持稳定的场景，请使用您自己的域名。

## 部署

请先查看所有即将发送的内容。 `plan` 不会向任何服务提供商或 Cloudflare 发起请求：

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

然后使用相同的选项和凭据进行部署：

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

初始服务器类型： `cpx22` (Hetzner)， `s-1vcpu-2gb` (DigitalOcean)， `g6-standard-1` (Linode)， `vc2-1c-2gb` (Vultr)， `t3.small` (AWS)。 `--location` 以及 `--image` 默认使用各 服务商位于欧洲区域的 Ubuntu 24.04 系统。

`--repository` 从另一个 https Git 仓库获取提交，且 URL 中不包含凭据 （默认 `https://github.com/phishdestroy/TgWitness.git`). `deploy` 也接受 `--out` 指定其他部署目录（默认 `deployments/NAME`；若目录中已存在 部署则会被拒绝）以及 `--wait`，即等待收集器签署声明所需的分钟数： 1 到 240，默认值为 20，或 60 用于 `generic`.

命令：

1. 创建一个 Cloudflare 隧道，其入站流量将面板主机名转发至面板， 若已指定，则将见证主机名转发至 `/api/witness/head` 并 `/api/assurance` 且仅限该主机名；
2. 为这些主机名创建代理 CNAME 记录，并拒绝已存在的名称；
3. 创建一个不包含入站规则的提供商防火墙，并在其后部署一台服务器，该服务器不使用 SSH 密钥、 不进行备份、不使用控制台代理，且 cloud-init 会屏蔽 SSH、锁定 root 权限，并安装 `cloudflared`、精确获取该提交、验证并以 强化版 systemd 服务的形式启动 TgWitness；
4. 等待收集器发送的签名声明，并验证该声明是否指明了此服务器以及 此 cloud-init 的哈希值。

`deployments/case-2026-11/` 其中包含：

| 文件 | 目录 | 分享？ |
| --- | --- | --- |
| `deployment.json` | ID、哈希值、发出的 API 调用（方法、路径、状态）以及第一条已签名的声明 | 是的，通过验证器 |
| `cloud-init.redacted.yaml` | 将云初始化脚本（cloud-init）中的两个密钥替换为 `REDACTED` | 是 |
| `panel-token.txt` | 面板令牌 | 无 |

提供商的根密码、隧道令牌和面板令牌绝不会写入 `deployment.json`。请通过您无法单独控制的频道（例如见证频道或发送给收件人的消息）发布文末显示的收集器指纹。

请使用面板令牌登录 Telegram， `https://case.example.org` 使用面板令牌登录 Telegram，具体操作参见 [账户指南](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/)。面板操作会被记录在已签名的日志中；这些操作并非 SSH 会话。[见证人](https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/)可以轮询 `https://case-witness.example.org`.

不支持 SSH：如果初始化失败，收集器将永远不会响应。请删除服务器并 重新部署，或使用调试部署来查找原因。

### 用户数据中的秘密

cloud-init 包含两个密钥：控制面板令牌和 Cloudflare 隧道令牌。 签名密钥不在此列；它是在服务器上生成的。Hetzner、DigitalOcean 和 Linode 不会通过其 API 返回用户数据。Vultr 会将其返回给任何能够读取 实例的密钥，而 EC2 则通过 `DescribeInstanceAttribute`。对于 AWS，仅向验证者提供表格中的三项 操作，切勿 `ec2:Describe*`。对于 Vultr，假设验证者的密钥可以读取这两个 令牌。隧道令牌允许某人运行第二个连接器： `verify` 这会报告任何 不在服务器上的连接器，且收集器的声明无法通过这种方式伪造，因为每一条 都会对新的挑战进行签名。使用 `--quick-tunnel` 第二个密钥则是地址密钥： 任何读取它的人都可以发布一个虚假地址，而控制面板会接受该地址。

该收集器的公开声明中未提及服务器地址和登录来源； 这两项信息均保存在已签名的日志中。

## 调试部署与锁定

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` 仅支持来自单一地址 或小型网络（IPv4 最多 /24，IPv6 最多 /48）的单个密钥的 SSH 连接。 `KEY` 已向 服务商注册：Hetzner 项目中 SSH 密钥的名称或 ID、DigitalOcean 团队中 SSH 密钥的 ID 或指纹、其个人资料中的 SSH 密钥已添加到 root 用户的 Linode 用户名、 Vultr 账户中 SSH 密钥的 ID，或该区域内 EC2 密钥对的名称。这些 选项不适用于 `generic`。此类部署将被记录为 `debug` ，且**绝不会**被报告为 高可信度。操作完成后，请运行 `sudo tgwitness-lock` 作为最后一次 SSH 会话的最后一条命令，然后：

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

防火墙会丢失所有入站规则。随后生成的报告会显示何时允许了 SSH 连接以及何时 将其关闭；该窗口将保持可见状态。

## 删除部署

`destroy` 删除服务器及其防火墙（通过部署标签定位），以便 中途失败的部署也会被移除，随后删除指向其 隧道的 DNS 记录以及隧道本身。服务器的日志和签名密钥将一并删除：请先导出 证据。记录将保留，并标记为 `removed`，并附有删除操作的API调用记录。

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

针对 Hetzner，已通过 API 实现了内容删除功能。对于其他服务商 `destroy` 在删除任何内容之前 需先停止服务，并在服务商控制台中指定要删除的标签。手动安装的 服务器（`generic`）仅会丢失其隧道和 DNS 记录。快速隧道部署无需 Cloudflare 令牌：其隧道仅连接至服务器，且相关帖子将在 ntfy.sh 上于 12 小时内过期。

## 任意服务器（自我认证）

`--provider generic` 适用于购买或手动安装的服务器。 `deploy` 用于创建隧道 和 DNS，并写入 `install.sh` （私有）和 `install.redacted.sh` （用于发布），然后进入等待状态。 将 `install.sh` 到新安装的 Ubuntu 24.04 服务器上，并在该服务器上运行：

```
sudo bash install.sh
```

它会记录主机当时的原始状态（登录信息、账户、 `authorized_keys`、监听套接字、 服务、定时任务、软件包）的原始状态，安装该提交，启用主机防火墙，删除 自身，屏蔽 SSH 并结束会话。此类服务器的报告充其量只能 **算是“自我证明”**：无论谁运行了安装程序，在运行之前都已拥有 root 权限，且验证者无法获取 任何提供商记录。但这仍优于来源不明的服务器：资产清单、 安装程序哈希值以及此后每次登录都经过了签名。

## 验证

验证者需要 `deployment.json`已发布的安装程序、只读凭据，以及 最好是该提交的代码检出和证据 ZIP：

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

验证器会在该时刻请求每个提供商和 Cloudflare 的值；记录 仅提供需要查询的 ID。退出代码 0 表示通过**（PASS）**，1 表示**失败（FAIL）**，2 表示 **待审核（REVIEW）**、**不完整（INCOMPLETE）**或**自我认证（SELF-ATTESTED）**。 `--fingerprint` 应来自一个独立的 频道；若无此信息，则仅将密钥与运营商的记录进行比对。 `python verify.py` 仍会像“[证据](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/)”部分所述那样，自行验证证据ZIP。

提供商操作分为以下几类：创建操作以及在创建后 30 分钟内启动的操作均通过审核； 控制台、救援、密码重置、重建、ISO、镜像、快照、备份、系统管理器、 EC2 实例连接和防火墙开放操作若失败；电源操作以及任何意外操作 均会被标记为待审查。未知操作绝不会悄无声息地通过审核。

## 证据移交报告

`--report report.md` 生成 Markdown 报告，并 `report.json` 其旁边：

1. 结果、收集器密钥指纹、部署、提供商、提交、服务器、防火墙、隧道；
2. 每次检查及其状态和来源（提供商 API、Cloudflare API、收集器声明、 证据日志）；
3. 提供者日志，其中包含每项操作的评估结果，以及（若提供者进行了记录）操作执行者；
4. Cloudflare 端点，用于存储隧道的连接信息、配置和审计日志；
5. 经签名的收集者声明；
6. 该报告阐明了哪些内容，又未阐明哪些内容；
7. 用于重现该功能的命令，以及每个输入文件的SHA-256。

提交报告、 `report.json`, `deployment.json`、已发布的安装程序以及 证据 ZIP。请尽早生成报告：服务商的日志保存期限有限。

## Cloudflare 作为外部见证方

此处所有内容均为可选。即使没有 Cloudflare 账户，服务器仍可运行，且其中两项 功能目前已可正常使用：

| 内容 | 功能展示 | 在 TgWitness |
| --- | --- | --- |
| 快速隧道或您域名的隧道 | 该面板仅可通过隧道访问 | 服务器向导，参见上文 |
| drand 中继 `drand.cloudflare.com` | drand 轮之后生成的记录比它更新：日志是边进行边撰写的 | 证据模式、**更多见证者**、无账户（[格式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)） |
| 隧道状态通知 | 当隧道中断时，通过电子邮件或来自 Cloudflare 的 Webhook 通知 | 在 Cloudflare 控制台中进行设置 |
| 网关 DNS（`--gateway-dns`，或在向导中称为 **Cloudflare Gateway DNS**） | 服务器查询的每个名称，均由 Cloudflare 通过 TLS 响应；Hetzner 防火墙不允许 DNS 访问其他任何内容；网关策略是否可以重写响应 | Hetzner，免费“零信任”套餐，不提供域名； `verify` 检查防火墙、位置、日志记录、策略、服务器查询及审计日志；证据模式会将日志复制到日志簿中 |
| 与 Cloudflare 的网关：服务器上运行一个客户端，并配置出站防火墙，仅允许连接 Cloudflare | 服务器建立的每次连接，而不仅仅是 DNS 连接 | 尚未开发 |
| 面板前方的访问入口 | 谁在何时登录了该面板 | 尚未实现：需要您自己的域名 |
| SSH 命令日志记录 | 调试会话中的每个命令 | 尚未开发 |

Logpush（该功能会将 Cloudflare 的副本保存在 R2 中）是一项企业级功能：在免费 套餐中，Cloudflare 会 `logpush is not enabled for this account`。其网关日志在该处保留 24 小时，因此“证据模式”会将其复制到已签名的日志中（即 **Cloudflare Gateway 记录的 该服务器的 DNS 查询日志**，这是一个具有“账户分析读取”权限的只读令牌）。

如果没有“零信任”方案，一个账户只有一个 DNS 位置。当 Cloudflare 拒绝另一个位置时， 服务器会共享现有的位置，并通过其地址来区分查询；该过滤器 也需要“零信任”PII 读取权限，并且 `destroy` 这会留下一个共享位置。一次日志查询的跨度 最多为三小时，因此复制和 `verify` 读取操作需在三小时的时段内完成。

Gateway DNS 负责系统解析器。通过 443 端口以 DNS over HTTPS 方式连接至其他解析器，以及 连接至未被任何地方查询的地址（例如 Telegram 的数据中心）的连接，均不会 记录在日志中。

Cloudflare 无法查看 Telegram 的加密内容、该 Telegram 账户下的其他设备 （“证据模式”的设备列表是从 Telegram 端记录的）或服务提供商的虚拟机管理程序。

## 阅读部署结果

For an ordinary VM, the provider controls the host infrastructure, and local inventory is checked alongside provider records. For Intel TDX, the verifier additionally checks the hardware quote, collector binding, compose and OS measurements. Read the individual results to see which checks passed or were unavailable.

Historical firewall detail depends on the provider; Linode retains rule versions. The [validation record](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/) lists tested deployments and remaining live checks, and [verification scope](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope) connects these environment checks to archive acquisition and integrity.
