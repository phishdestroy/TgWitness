# 已测试的内容

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/

Telegram 实时测试、自动化检查、浏览器检查以及尚未经过验证的内容。

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

## 剩余资格要求

该保留的实时日志记录了实际的收集、编辑、删除通知、附件、 复核以及速率限制处理。 它并不记录详尽的送达情况，也不记录受控的 角色可见性矩阵、响应方、长时间的 FloodWait、账号封禁以及 网络/进程中断恢复情况。QR 令牌的发放与已完成的 移动端 QR 确认仍属不同流程。

Docker 构建/运行、Linux/macOS 安装、持续高负载、独立安全 审查、真正的独立 TSA 响应、证书撤销/归档验证以及 取证认证仍不在记录的资质范围内。已实现 MTProto 状态 保存和补录功能；原子级持久化重放功能尚未建立。 管理日志 收集、额外反应堆列表以及优先级短轮询仍为独立功能。 有关受控资格认证矩阵，请参阅[实时验收](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)报告。

本地详细记录和截图位于 test-results/ 目录下（Git 已忽略）。 docs/assets/ 目录中的公开截图仅包含虚构的演示数据。
