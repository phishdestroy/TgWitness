# 已测试的内容

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/

Telegram 实时测试、自动化检查、浏览器检查以及尚未经过验证的内容。

Each result below applies to its recorded revision and environment. The [current capability matrix](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) separates implementation, published downloads and remaining qualification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Phala Cloud 实时部署 · 2026年11月4日

`--provider phala --quick-tunnel` 在真实的 **Phala Cloud**（`tdx.small`，区域 US-WEST-1）上运行，使用了一个空工作区的 Phala Cloud API 密钥、真实的 ntfy.sh、GitHub 以及 Intel PCS。 CVM 安装了提交 `df7d860c`（v0.8.1）；部署、验证和销毁操作均通过命令行执行， 并应用了以下修复方案。七台 CVM 的总费用约为 1.9 美分。

前两次部署发现了与模拟的 Phala Cloud 存在五处差异。 [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) 现在可以重现每处差异，若未进行修复则会失败：

| 在 Phala Cloud 上 | 修复之前 | 修复 |
| --- | --- | --- |
| 必须提供 `compose_file.name` | HTTP 422，未创建任何内容 | Docker Compose 配置中包含 CVM 的名称 |
| 除非指定为空，否则 Phala 会向被测的 app-compose 中添加其自身的预启动脚本（v0.0.20：Docker 登录、`docker compose pull`、root 密码、来自 `user_config` 的 SSH 密钥） | `tdx_compose` 失败：代码超出已发布的 Docker Compose 配置范围 | app-compose 将 `pre_launch_script` 设置为 `""`；Phala 随后将其省略 |
| 若未指定 `image`，Phala 将选择 `dstack-dev-0.5.12`（开发版），该版本已启用 SSH 访问 | `server_state` 失败。该镜像仅硬件认证记录通过；仅提供商记录和 `tdx_os` 显示了该信息 | 部署过程要求使用 Phala 当前版本（`dstack-0.5.12`）的生产构建版本 |
| 当 dstack 网关关闭时，CVM 详细信息中从未出现 `instance_id` | 部署等待 30 分钟后失败 | 实例 ID 读取自 CVM 状态 |
| 重启、停止和启动属于 CVM 操作，而非应用程序修订 | `provider_actions` 未列出重启记录 | 这些操作也包含读取操作 |

第三次部署：

- 该 CVM 在关闭 SSH 访问的情况下运行了 `dstack-0.5.12`。收集器在创建后约 1.5 分钟发布了其签名地址。随后部署通过了 `tdx_binding`、`tdx_quote`（Intel TCB UpToDate、硬件认证记录 v4、FMSPC `20a06f000000`，非调试模式，不可迁移，支持从英特尔获取的加密验证数据 ），`tdx_compose_hash`、`tdx_compose`（字节级比对）以及 `tdx_identity`（KMS 密钥）。
- 访问 trycloudflare.com 地址的控制面板在未提供令牌或提供错误令牌时返回 401 状态码， 而使用控制面板令牌时返回 200 状态码。
- `verify`，其中 `--source` 指向 GitHub 上的该提交存档，且指纹已单独通过： 服务器、`server_state`、防火墙（无网关，无公共端点）、提供商日志、 账单、指纹、源哈希、启动以及五项 `tdx_*` 检查均通过。 Cloudflare 和 `tdx_os` 不可用，因此结果为“不完整”。
- 通过 Phala 的 API 进行了两次重启：每次 CVM 都在两分钟内恢复运行，使用 相同的收集器密钥，生成新的签名地址，而旧地址则返回 530 状态码。`verify` 将 此次新启动及两次重启均报告为 REVIEW。 通过 `--evidence`，它确认了日志 签名以及三次启动，每次启动均带有来自同一 CVM 的独立 Intel TDX 硬件认证记录。
- `destroy` 仅删除了该 CVM。随后工作区变为空，且控制面板地址停止 响应。
- 控制面板向导的价格查询显示 `tdx.small` 的价格为每小时 0.058 美元。若 API 密钥错误，则会显示简单的 “未接受该 API 密钥”提示信息。

另外两项发现，已随后修复：

- 在没有地址密钥的情况下，`verify` 遵循了关于该地址主题的最新格式正确的帖子， 该帖子印在已发布的 Docker Compose 配置中。一条伪造的帖子将其发送到一个不 存在的宿主机，导致 `statement` 失败：伪造者无法冒充收集器，但可以阻断 第三方验证，利用伪造的未来时间戳最长可阻塞长达 12 小时。收集器现在 还会发布使用自身密钥签名的地址，当 收集器发布此类消息时，`verify` 仅接受此类消息，且消息按 ntfy.sh 的接收时间排序。 [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) 重放了伪造的发布。CVM 仅从包含该代码的提交中运行此代码，因此本次运行的收集器尚未对其地址进行签名， `verify` 也指出了这一点。
- `tdx_os` 原先依赖 `dstack-mr`，而该工具当前版本提供的是 `measure-os`，并非文档中提到的 `measure --json`。验证器现在会根据已发布的镜像和虚拟机配置（包括 ACPI 表）自行计算 MRTD 和 RTMR0-2。

第四次部署包含以下内容：

- 部署过程曾一次下载已发布的 `dstack-0.5.12`，将其与 CVM 报告的操作系统镜像哈希值进行比对，而 `tdx_os` 通过验证：MRTD、RTMR0、RTMR1 和 RTMR2 均与针对 QEMU 8.2.2、1 个 vCPU 和 2 GiB 环境下计算出的值。同样的计算在宣称的 4 GiB、2 个 vCPU、 QEMU 9.2.1 或第二张网卡的情况下，得出的 RTMR0 值不同；而在内核、固件或命令行发生变更 以及使用开发镜像时，则会失败。
- `verify` 通过了全部 16 项检查（包括快速隧道的连接器），因此结果 为“通过”。 它生成 HTML 和 PDF 证书，并使用签名和时间戳进行数字加封，其中包含来自 比利时政府时间戳单元 TSU 202301（已列入比利时可信 列表）的合格 eIDAS 时间戳、FreeTSA 时间戳以及验证者的签名；`check-report` 确认了所有这些 内容以及 PDF 文件的签名。
- 重启后，`verify --evidence` 确认了两次启动，每次都伴随着在 CVM 内部生成的硬件认证，且每次 均从已发布的 `dstack-0.5.12` 启动；重启和新启动均处于 REVIEW 状态。
- `destroy` 使工作区保持为空。

第五次部署运行了来自提交 `53a0f7e9` 的收集器，其中包含上述所有内容：

- 收集器在其地址旁发布了使用自身密钥签名的地址，紧邻操作员的 HMAC 帖子。 随后，该主题中被添加了两条伪造的帖子，一条 HMAC 值为零，另一条由另一个 Ed25519 密钥签名，两者均声称时间在 2096 年。 `verify` 采用了由 收集器密钥签名的地址，并通过了全部 16 项验证；该印章再次包含经认证的比利时时间戳、 FreeTSA 的时间戳以及验证者的签名，而 `check-report` 对此予以确认。
- 重启后，收集器发布了经签名的全新地址：`verify` 立即检测到该地址， 运营商 **通过 HMAC 发布在 27 秒后检测到当前地址**，两者均忽略了 伪造的发布。`verify --evidence` 确认有两个实例从 `dstack-0.5.12` 启动。
- 部署过程显示了 Phala 对 CVM 的计费金额（含磁盘费用）：每小时 0.06078 美元。

面板向导在 Phala Cloud 上运行了两次，一次通过其任务 API，一次通过 基于真实 Chromium 内核的浏览器：价格核查、在 **Advanced** 下提交创建，全部六项 认证检查均通过，服务器列表显示了计费价格（每月 44.37 美元）， **Find 当前地址**、下载已测量的 Docker Compose 配置以及删除操作。浏览器未出现任何页面错误。 此后，工作区每次均处于空状态。

未涵盖内容：Phala 上的 Cloudflare 域名、CVM 上的 Telegram 账户以及 `dstack-0.6.1` 镜像。向导在创建前的报价仅包含 Phala 的计算费用，因为其 API 仅针对现有 CVM 列出磁盘 费用；服务器列表显示的是创建后的实际计费金额。

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | 计数 |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| 检查 | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

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

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

本地详细记录和截图位于 test-results/ 目录下（Git 已忽略）。 docs/assets/ 目录中的公开截图仅包含虚构的演示数据。
