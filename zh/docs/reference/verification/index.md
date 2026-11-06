# 已测试的内容

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/

Telegram 实时测试、自动化检查、浏览器检查以及尚未经过验证的内容。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文档](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [证据与验证](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/)

![证据与验证](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**更新 6 11月 2026.** 结果与每次运行所记录的修订版本、环境和 工作负载相关联。 [当前功能](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) 描述了 可用的工作流；本页面记录了实际已检查的内容。

[性能图表](https://phishdestroy.github.io/TgWitness/docs/validation/) · [经签名的英文审核报告](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [可下载的测量数据](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| 最新证据 | 结果 | 范围 |
| --- | --- | --- |
| 版本审计 · 11月6日 | 1,461个核心测试通过；37个平台测试跳过 | 源代码 `92e539af40d8`；保留已公开的调查结果 |
| 最新导出 · 11月6日 | 127.713 和 141.781 条记录/秒，完整周期 | 每台服务器限两个账户；文本和元数据通过 WARP 传输 |
| 保留的存档 · 11月6日 | 48个归档文件；已验证3,598,381条记录 | 已根据固定工作区密钥对现有存档进行了核对 |
| Trusted Live · 11月5日 | 受保护的 CPU 记录和 WARP 检查 | 官方桌面版登录和原生导出功能仍未实现 |
| Phala / Intel TDX · 11 月 4 日 | 后续运行中通过了所有16项验证器检查 | 历史部署；CVM 上没有 Telegram 账户 |

**本页内容**

- [版本审核与最新导出 · 6年11月2026日](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu 和 WARP · 5年11月2026日](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Phala Cloud 实时部署 · 4年11月2026日](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [实时服务器日志清单 · 1年11月2026日](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [最近的离线和故障注入检查 · 1年11月2026日](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Telegram 实时测试，完整账户 · 29年10月2026日](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [使用 libarchive 打开的受密码保护的导出文件 · 29年10月2026日](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Telegram 实时测试 · 2026年10月27日至29日](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [合成本地容量测量](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#synthetic-local-capacity-measurement)
- [对一百万条消息进行全文搜索 · 5年11月2026日](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [剩余说明](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/#remaining-qualification)

## 版本审核与最新导出 · 6年11月2026日

本次审计基于源代码 v0.9.1 `92e539af40d8368d198ff5e040f1d876f2c1310e`，发布版本 `92e539af40d8-83e41104669e`。三个 服务器上的已安装包烟雾测试均通过。签名报告保留了当时观察到的状态。

[![两项新工作负载的采集率和完全导出率](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| 工作量 | 记录 | 获取 | 完整周期 | 完整周期率 |
| --- | --- | --- | --- | --- |
| 服务器 A · 两个账户 | 27,030 | 189.043秒 | 211.647秒 | 127.713条记录/秒 |
| 服务器 B · 两个账户 | 29,299 | 182.513秒 | 206.650秒 | 141.781条记录/秒 |

两次导出均未启用续传功能，排除了附件和头像，且最终 未产生任何重复或重复使用的记录。完整周期包括准备、 采集、筛选、打包和归档验证。服务器 A 还执行了 受保护聊天读取检查。服务器 A 上发生了四次 FloodWait 事件，服务器 B 上发生了三次， 均被正确处理。这些观察结果并不构成普遍的吞吐量保证。

| 检查 | 结果 | 资格要求 |
| --- | --- | --- |
| 核心 pytest | 1,461 条通过 | 37个平台跳过 |
| 浏览器 / 浏览器用户体验 / 证据 / 网站 | 102 / 66 / 15 / 9 通过 | 这些程序与其他测试存在重叠；计数结果不可相加 |
| Capture 插件 | 124 条通过 | 三项官方网页验证因必需的 Chromium 沙箱而被阻止 |
| API 授权 | 269条路由；538个请求通过 | 凭证缺失和访问权限被撤销 |
| 保留的存档 | 48/48 已验证 | 3,598,381条记录；已固定的工作区密钥 |
| 实时车队读取检查 | 40 个配置文件中有 24 个通过验证 | 16条WARP路由未通过资格认证；这些配置文件未建立连接 |

该[签名报告](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md)记录了所有已公开的 发现结果，包括未发布秘密聊天快照中的三个缺陷，这些缺陷 在经过审计的主构建版本中并不存在。先前的 [公开历史](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md)验证使用了不同的 版本和工作负载；其比率不得与本次比较结果合并。

使用 [固定密钥和验证器](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files)验证原始报告。 其签名可防止操作员的报告被篡改。但这并非 独立认证、Telegram 作者身份证明或 GDPR 认证。

## Trusted Live CPU Ubuntu 和 WARP · 5年11月2026日

保留的集成运行使用了一个仅基于 CPU 的 Ubuntu 24.04.5 客户机（4 个 vCPU，8 GiB） ，该客户机在 RunPod CPU 主机内的 QEMU 环境中运行。收集器使用 `14e642a5`；验证使用 `02072461`。最终的修复程序合并到 [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) 中，提交 ID 为 `755f78f6`，其代码树与测试的 PR 头一致。这并非 TEE 环境。

- 一个真实的 WARP 连接器报告状态正常；代理的 HTTPS 报告 WARP 和网关 已启用。三个探针观察到相同的出站地址，这并不保证是固定 IP。
- 断开 WARP 连接导致代理请求失败。直接连接网关服务的 HTTPS 请求被拒绝。在记录器命名空间中，直接的 IPv4/IPv6 连接、外部 DNS 以及 Docker 的嵌入式 UDP 解析器均被阻止。
- 一个具有范围限制的只读提供商令牌可以读取健康状态/连接信息，但无法 读取连接器注册令牌。已签名的提供商观察结果中包含 明确标记为不可用的样本。由于该见证程序运行在运营商的主机上，因此这 证明了记录和保留功能，而非独立的第三方托管。
- 官方桌面版已进入未认证的欢迎界面。在捕获过程中，受保护的键盘 输入被拒绝。解码了三个 H.264 显示片段，并 检查了其时钟叠加层。对包含 18 个事件的预检存档进行了验证， 验证依据为固定的记录器密钥和保留的检查点。
- 最终的捕获测试在 Windows 和 Linux 持续集成（CI）环境中通过了 114 个用真实 Chromium/FFmpeg 实现的测试用例。五项基准测试和依赖项建议检查均通过。

初始配置的 2 个 vCPU/4 GiB 环境在并发构建镜像的负载下超时， 并通过防护机制停止运行；此情况不计为成功。手动测试账户 登录、原生聊天记录导出、真实混合模式对比以及 Telegram 端注销操作仍 待完成。未导入任何提供的 Telethon 会话。附件、自动 OCR、 本地 drand BLS 验证以及 Trusted Live TDX 认证均未通过验证。

## Phala Cloud 实时部署 · 2026年11月4日

**历史结果：**后续部署通过了全部16项验证器检查， 包括英特尔 TDX 和快速隧道。重启证据、签名地址 发现以及报告时间戳均进行了单独检查。每个测试 CVM 在 运行结束后均被移除。

| 设置 | 记录值 |
| --- | --- |
| 提供商 | Phala Cloud · `tdx.small` · US-WEST-1 |
| 部署 | `--provider phala --quick-tunnel`；初始工作区为空 |
| 初始收集器 | `df7d860c` · v0.8.1 |
| 包含所有修复程序的收集器 | `53a0f7e9` |
| 生产环境访客 | `dstack-0.5.12`；SSH 访问已禁用 |
| 外部服务 | ntfy.sh、GitHub 和 Intel PCS |
| 观测到的成本 | 七个 CVM，总计约1.9美分；历史测试定价 |

以下序列分别列出了初始故障、修复情况和已完成的检查。 这些 CVM 未连接任何 Telegram 账户。

**部署 1–2 · 提供商差异与回归测试**

前两次部署发现了与模拟的 Phala Cloud 存在五处差异。 [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) 现在可以重现每处差异，若未进行修复则会失败：

| 在 Phala Cloud 上 | 修复之前 | 修复 |
| --- | --- | --- |
| 必须提供 `compose_file.name` | HTTP 422，未创建任何内容 | Docker Compose 配置中包含 CVM 的名称 |
| 除非指定为空，否则 Phala 会向被测的 app-compose 中添加其自身的预启动脚本（v0.0.20：Docker 登录、`docker compose pull`、root 密码、来自 `user_config` 的 SSH 密钥） | `tdx_compose` 失败：代码超出已发布的 Docker Compose 配置范围 | app-compose 将 `pre_launch_script` 设置为 `""`；Phala 随后将其省略 |
| 若未指定 `image`，Phala 将选择 `dstack-dev-0.5.12`（开发版），该版本已启用 SSH 访问 | `server_state` 失败。该镜像仅硬件认证记录通过；仅提供商记录和 `tdx_os` 显示了该信息 | 部署过程要求使用 Phala 当前版本（`dstack-0.5.12`）的生产构建版本 |
| 当 dstack 网关关闭时，CVM 详细信息中从未出现 `instance_id` | 部署等待 30 分钟后失败 | 实例 ID 读取自 CVM 状态 |
| 重启、停止和启动属于 CVM 操作，而非应用程序修订 | `provider_actions` 未列出重启记录 | 这些操作也包含读取操作 |

**部署3 · 认证、访问检查和重启证据**

- 该 CVM 在关闭 SSH 访问的情况下运行了 `dstack-0.5.12`。收集器在创建后约 1.5 分钟发布了其签名地址。随后部署通过了 `tdx_binding`、`tdx_quote`（Intel TCB UpToDate、硬件认证记录 v4、FMSPC `20a06f000000`，非调试模式，不可迁移，支持从英特尔获取的加密验证数据 ），`tdx_compose_hash`、`tdx_compose`（字节级比对）以及 `tdx_identity`（KMS 密钥）。
- 访问 trycloudflare.com 地址的控制面板在未提供令牌或提供错误令牌时返回 401 状态码， 而使用控制面板令牌时返回 200 状态码。
- `verify`，其中 `--source` 指向 GitHub 上的该提交存档，且指纹已单独通过： 服务器、`server_state`、防火墙（无网关，无公共端点）、提供商日志、 账单、指纹、源哈希、启动以及五项 `tdx_*` 检查均通过。 Cloudflare 和 `tdx_os` 不可用，因此结果为“不完整”。
- 通过 Phala 的 API 进行了两次重启：每次 CVM 都在两分钟内恢复运行，使用 相同的收集器密钥，生成新的签名地址，而旧地址则返回 530 状态码。`verify` 将 此次新启动及两次重启均报告为 REVIEW。 通过 `--evidence`，它确认了日志 签名以及三次启动，每次启动均带有来自同一 CVM 的独立 Intel TDX 硬件认证记录。
- `destroy` 仅删除了该 CVM。随后工作区变为空，且控制面板地址停止 响应。
- 控制面板向导的价格查询显示 `tdx.small` 的价格为每小时 0.058 美元。若 API 密钥错误，则会显示简单的 “未接受该 API 密钥”提示信息。

**后续修复 · 签名地址发现与操作系统测量**

- 在没有地址密钥的情况下，`verify` 遵循了关于该地址主题的最新格式正确的帖子， 该帖子印在已发布的 Docker Compose 配置中。一条伪造的帖子将其发送到一个不 存在的宿主机，导致 `statement` 失败：伪造者无法冒充收集器，但可以阻断 第三方验证，利用伪造的未来时间戳最长可阻塞长达 12 小时。收集器现在 还会发布使用自身密钥签名的地址，当 收集器发布此类消息时，`verify` 仅接受此类消息，且消息按 ntfy.sh 的接收时间排序。 [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) 重放了伪造的发布。CVM 仅从包含该代码的提交中运行此代码，因此本次运行的收集器尚未对其地址进行签名， `verify` 也指出了这一点。
- `tdx_os` 原先依赖 `dstack-mr`，而该工具当前版本提供的是 `measure-os`，并非文档中提到的 `measure --json`。验证器现在会根据已发布的镜像和虚拟机配置（包括 ACPI 表）自行计算 MRTD 和 RTMR0-2。

**部署4 · 所有16项检查、报告封条及重新启动验证**

- 部署过程曾一次下载已发布的 `dstack-0.5.12`，将其与 CVM 报告的操作系统镜像哈希值进行比对，而 `tdx_os` 通过验证：MRTD、RTMR0、RTMR1 和 RTMR2 均与针对 QEMU 8.2.2、1 个 vCPU 和 2 GiB 环境下计算出的值。同样的计算在宣称的 4 GiB、2 个 vCPU、 QEMU 9.2.1 或第二张网卡的情况下，得出的 RTMR0 值不同；而在内核、固件或命令行发生变更 以及使用开发镜像时，则会失败。
- `verify` 通过了全部 16 项检查（包括快速隧道的连接器），因此结果 为“通过”。 它生成 HTML 和 PDF 证书，并使用签名和时间戳进行数字加封，其中包含来自 比利时政府时间戳单元 TSU 202301（已列入比利时可信 列表）的合格 eIDAS 时间戳、FreeTSA 时间戳以及验证者的签名；`check-report` 确认了所有这些 内容以及 PDF 文件的签名。
- 重启后，`verify --evidence` 确认了两次启动，每次都伴随着在 CVM 内部生成的硬件认证，且每次 均从已发布的 `dstack-0.5.12` 启动；重启和新启动均处于 REVIEW 状态。
- `destroy` 使工作区保持为空。

**部署5 · 由收集器签名的发现机制与伪造帖子的拒绝机制**

收集器从提交`53a0f7e9`开始运行，该提交包含了上述修复内容。

- 收集器在其地址旁发布了使用自身密钥签名的地址，紧邻操作员的 HMAC 帖子。 随后，该主题中被添加了两条伪造的帖子，一条 HMAC 值为零，另一条由另一个 Ed25519 密钥签名，两者均声称时间在 2096 年。 `verify` 采用了由 收集器密钥签名的地址，并通过了全部 16 项验证；该印章再次包含经认证的比利时时间戳、 FreeTSA 的时间戳以及验证者的签名，而 `check-report` 对此予以确认。
- 重启后，收集器发布了经签名的全新地址：`verify` 立即检测到该地址， 运营商 **通过 HMAC 发布在 27 秒后检测到当前地址**，两者均忽略了 伪造的发布。`verify --evidence` 确认有两个实例从 `dstack-0.5.12` 启动。
- 部署过程显示了 Phala 对 CVM 的计费金额（含磁盘费用）：每小时 0.06078 美元。

### 面板向导和剩余范围

面板向导在 Phala Cloud 上运行了两次，一次通过其任务 API，一次通过 基于真实 Chromium 内核的浏览器：价格核查、在 **Advanced** 下提交创建，全部六项 认证检查均通过，服务器列表显示了计费价格（每月 44.37 美元）， **Find 当前地址**、下载已测量的 Docker Compose 配置以及删除操作。浏览器未出现任何页面错误。 此后，工作区每次均处于空状态。

未涵盖内容：Phala 上的一个 Cloudflare 域名、CVM 上的一个 Telegram 账户，以及 `dstack-0.6.1` 镜像。创建前的向导价格仅为 Phala 的计算价格，因为其 API 仅列出了现有 CVM 的磁盘 价格；服务器列表显示的是创建后的计费价格。 本节中的所有价格均于 4 年 2026 月 4 日观察到。

## 实时服务器日志清单 · 1年11月2026日

大约在协调世界时（UTC）19:15，通过顺序只读 SQLite `query_only` 查询统计了 运行中服务器上十个工作区数据库中的事件数量。在查询期间， 数据收集仍在继续，因此这并非跨工作区的原子快照。

| 在十个工作区数据库中观察到 | 计数 |
| --- | --- |
| 包含至少一个`message.new`事件的工作区 | 8 |
| 日志记录，包括操作事件 | 1,610,818 |
| `message.new`事件 | 900,232 |
| `message.edited`事件 | 80,683 |
| `message.deleted`事件 | 400,536 |
| `message.recovered`事件 | 53,403 |
| `message.snapshot`事件 | 2,183 |
| `media.saved`事件 | 50,418 |
| `media.failed`事件 | 5,575 |
| `coverage.gap`事件 | 11 |
| 数据库字节数（不包括 WAL 文件和媒体文件） | 7,909,003,264 |

这些是 **事件计数**，而非唯一的消息、用户或媒体文件。同一 条消息可能出现在多个工作区中，且编辑或删除操作可能会产生 另一个日志事件。 `media.failed` 统计的是历史故障事件，而非 当前的媒体队列。这些查询 **不** 重新验证签名以及所有 记录的完整 1,610,818 记录，未测量投递情况或吞吐量，也未证实 每个 Telegram 事件均已被捕获。此处未发布任何消息内容、账户或聊天 ID、 工作区标签、凭据或私有文件。

在本次审查中，单独配置的公共监控器覆盖了三个数据源： 其中一个捕获响应状态为OK，另外两个报告为`no_response`。该监控器 并非十个工作区的健康状况汇总。`no_response`表示观察者无法 在该次检查中获得响应；这并不意味着消息丢失。下文所述的 10月29日规模较小的测试拥有其自身的明确签名和哈希链验证。

## 最近的离线和故障注入检查 · 1年11月2026日

这些检查使用的是虚构数据和本地文件；它们为 当前源文件提供了回归证据，而非针对其他实时 Telegram 投递测量的证据：

| 检查 | 测试内容 |
| --- | --- |
| [源代码存档](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | 两个源字节完全相同但文件时间已更改的构建版本，生成了相同的 ZIP 文件和校验和。压缩包的精确字节数和文件哈希值完全匹配；私有测试文件未被包含。模拟的写入失败操作并未影响之前的压缩包和校验和。 |
| [账户导出与恢复](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | 第二个 ZIP 成员上模拟的磁盘错误未留下任何已发布或部分的 ZIP 文件。恢复操作保持了每个签名收据的字节级一致性，使用预期的签名指纹生成了一个可独立验证的存档，并将合成的覆盖缺口作为部分结果保留下来。随着历史记录的增长，可扩展性断言可防止重复扫描任务和收据。 |
| [最小化信息披露以保护隐私](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | 在所有三种身份识别模式下，以及在文本缺失的情况下，均对合成 Unicode 名称和别名、嵌套元数据、未知发件人和媒体字段进行了检查。掩码限制失败并未悄然削弱信息遮蔽效果；原始的已签名账户导出文件保持不变。 |
| [Linux 多媒体解码器和 OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | 在提交`5a9e0814`时，[Linux Docker CI 检查](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192)通过了以下测试：生成 Ogg/Opus、MP3、M4A、带视频的 MP4、WAV 和 FLAC 输入文件；伪造时长和二级文件引用控制；以及 48 个变异解析器测试用例（34 个被拒绝，14 个在范围内解码成功）。真实的 Tesseract OCR 在原始字节不变的情况下运行。解码器和 OCR 在网络隔离的容器中运行，未使用 Whisper 模型。 |

这些检查在[拉取请求和](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) [完整检查](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml)工作流中运行。 它们测试的是这些故障边界，而非所有可能的存储故障，也并非测试 信息披露是否自动安全可发布。媒体检查不衡量 语音识别准确率或 Telegram 消息送达情况。分享前请审查每个衍生内容。

## Telegram 实时测试，完整账户 · 2026年10月29日

在以下测试结束后，该账户仍继续运行。10月29日12:10（UTC），其监控范围 被切换为整个账户（频道、群组、私人聊天和机器人）；控制面板要求 确认，经签名的日志记录了这一操作。截至17:59（UTC），日志中包含：

| 记录时间：10月27日 21:36 至 10月29日 17:59（UTC） | 计数 |
| --- | --- |
| 日志记录 | 9,968 |
| 新消息 | 5,308 |
| 在切换到完整账户后，其中的一部分 | 3,878 |
| 删除操作 | 784 |
| 其中部分消息在 TgWitness 保存后被删除 | 596 |
| 编辑 | 41 |
| 经复核后添加的消息 | 2,273 |
| 经重新核查已无法找到的消息 | 18 |
| 通过历史快照保存的消息 | 242 |
| 已保存的附件 | 247 |
| 收集器启动 | 19 |
| Telegram FloodWait 暂停 | 26 |

- 该小组的**“Verify”**核查确认了全部 9,968 条记录的签名和哈希链。
- 消息来自 2 个群组或频道以及 3 个私人聊天和机器人。在**“聊天”界面**中点击了一个消息按钮； 该请求及 Telegram 的响应均记录在日志中。
- 当收集器在重启后重新扫描该账户时，新增了聊天记录。由于 保存新聊天记录中早期消息的功能处于关闭状态（`history = 0`），因此本文不作讨论。

未涵盖内容：互动反应、成员变动、用户资料、发送消息、通过 邀请加入、代理服务器、通知、witness 机器人以及同时管理多个账户。公开文件 仅包含计数数据。

## 通过 libarchive 打开受密码保护的导出文件 · 2026年10月29日

由导出加密代码生成的归档文件（WinZip AES-256 格式，7-Zip 和 WinRAR 均可读取）使用 Windows 版 `tar`（bsdtar 3.6.2，libarchive）打开。 输入正确密码后， 解压后的文件与原始文件的 SHA-256 值一致；输入错误密码时，系统会显示“密码短语错误” 并拒绝解压。7-Zip 和 WinRAR 本身并未被调用。

## Telegram 实时测试 · 2026年10月27日至29日

一个真实的 Telegram 账户通过内置的 API 密钥对池登录，记录了 一个超级群组从 **10 月 27 日 21:36 UTC 至 10 月 29 日 05:15 UTC** 期间的活动。在此期间， 采集器共启动了 12 次。

| 已记录 | 计数 |
| --- | --- |
| 日志记录，包括心跳信息和服务记录 | 2,385 |
| 新消息 | 1,291 |
| 删除操作 | 472 |
| 其中部分消息在 TgWitness 保存文本后被删除 | 347 |
| 编辑 | 12 |
| 暂停期间遗漏的消息，经重新检查后已补充 | 12 |
| 已保存的附件 | 17 |
| 未下载附件（下载功能已关闭，或无文件可下载） | 14 |
| Telegram FloodWait 在重新检查期间会暂停，每次暂停 3 秒 | 8 |

- 所有 2,385 条记录的签名和哈希链均可通过日志的 公钥进行验证。
- 重启后，收集器将从保存的更新状态（`pts`）继续运行，Telethon 会进行补全；随后，重新检查会添加仍缺失的消息。
- 在每次 FloodWait 事件中，收集器都会等待指定时间，然后继续运行。
- 该账户保持登录状态，同一会话于 10 月 29 日重新连接。

本次测试未涵盖的内容包括：同时管理多个账户、管理员权限、代理服务器、 持续数小时以上的服务中断以及完整的[实时验收流程](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)。 公开文件仅包含以下统计数据：不包含任何账户或聊天标识符、消息内容或 凭据信息。

## 合成本地能力测量

命令：`python tools/check_capacity.py --events 10000 --chats 100`

| 指标 | 已观察到 |
| --- | --- |
| 输入 | 来自 100 个精选合成来源的 10,000 条合成消息事件 |
| 消息正文 | 400个字符；不含媒体或网络内容 |
| 数据采集 | 53.273 秒；187.7 次事件/秒 |
| 处理程序延迟 | p50 4.162 毫秒；p95 7.784 毫秒；最大值 129.118 毫秒 |
| ZIP 导出 | 启用 tracemalloc 后耗时 19.868 秒 |
| Python 导出分配的峰值追踪 | 0.51 MiB；不处理 RSS |
| ZIP 文件大小 | 4,610,962 字节 |
| 独立验证 | 所有 10,000 条事件均已通过验证 |

此工具测量的是该 Windows 主机上的本地序列化记录/导出路径。它 不测量 MTProto 传输、并发账户、Telegram 流量限制、媒体文件、 长期运行的工作负载，也不保证实际聊天数量。该测量结果早于 最终版离线时间戳工具的发布，而该工具不会改变所测量的消息路径。

## 对一百万条消息进行全文搜索 · 2026年11月5日

命令： `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

一个包含 200 个聊天群组中 1,000,000 条合成消息（俄语 词形、乌克兰语、英语、中文、日语、链接和用户名）的确定性签名日志，在 71 秒内完成索引；该索引占用 58 MiB 空间，此外还有 1.50 GiB 的日志文件。 最佳匹配 搜索耗时 9 至 190 毫秒（中位数），而之前的子字符串 搜索则需 2.4 至 3.2 秒。完整结果、硬件配置及限制：[全文搜索](https://phishdestroy.github.io/TgWitness/zh/docs/reference/search/#benchmark)。 `tools/test_fulltext.py` 还使用当前验证器对全文搜索之前生成的 （`tools/fixtures/evidence-before-fulltext.zip`）使用当前验证器进行验证，并使用该归档文件自身的 归档文件进行验证。 `verify.py`.

## 剩余资格要求

该保留的实时日志记录了实际的收集、编辑、删除通知、附件、 复核以及速率限制处理。 它并不记录详尽的送达情况，也不记录受控的 角色可见性矩阵、响应方、长时间的 FloodWait、账号封禁以及 网络/进程中断恢复情况。QR 令牌的发放与已完成的 移动端 QR 确认仍属不同流程。

Docker/Compose 及安装检查已记录在 CI 中；真实的 Phala 部署 和外部时间戳验证已在上文描述。这些并未建立 持续的高负载、完整的实时平台/角色矩阵、独立的安全 审查、长期归档验证或取证认证。已实现 MTProto 状态 保存和补发功能；原子无损实时重放功能尚未建立。 较新的回填功能可原子性地提交消息和游标，并保留可用的 近期操作，但其合成覆盖范围与实时资格认证有所不同。 有关受控资格认证矩阵，请参阅[实时验收](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)部分。

[公开审计目录](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md)仅包含 已签名的报告和汇总测量数据。详细的操作记录、 原始截图和账户资料仍属私有。位于 `docs/assets/` 中的应用程序截图使用的是虚构的演示数据。
