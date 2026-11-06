# 功能与限制

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/

TgWitness 的当前采集模型、多账户工作流、导出功能及操作边界。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文档](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Project reference](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Project reference](https://phishdestroy.github.io/TgWitness/assets/chapter-project.svg)

TgWitness 可保存已连接账户可访问的 Telegram 对话， 记录观察到的变更，并生成可验证的导出文件。本参考文档描述了 采集模型、当前工作流程及其边界。

**On this page**

- [Standalone application](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#standalone-application)
- [Shared investigations](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#shared-investigations)
- [Archive tools](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#archive-tools)
- [Optional extras](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#optional-extras)
- [Protocol and private sources](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#protocol-and-private-sources)
- [Multiple accounts](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#multiple-accounts)
- [Capture and attribution](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#capture-and-attribution)
- [Capacity and Telegram limits](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#capacity-and-telegram-limits)
- [Reliability and recovery](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#reliability-and-recovery)
- [Evidence model](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#evidence-model)
- [Export, deployment and handoff](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#export-deployment-and-handoff)
- [Stable release criteria](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/#stable-release-criteria)

## 独立应用程序

TgWitness 拥有独立的安装流程、数据目录和发布生命周期。随附的 Web 界面负责配置和审查；导出的记录可独立使用。

操作员连接其账户，选择彼此可见的消息源，并获取 一份保存的观察日志。控制面板展示内容、保存的更改、观察 来源以及已知的缺失信息。其他调查人员可以对导出的材料进行验证。

该面板区分了账户授权、对来源的访问权限、采集器 活动以及记录范围。在评估 消息较少或存在连接问题的时段时，请综合审查这些状态。

## 共享调查

管理员可签发作用域限定于工作区和 单个聊天的[访问令牌](https://phishdestroy.github.io/TgWitness/zh/docs/reference/access/)，并可设置按操作授权、IP 限制、有效期、登录次数限制 及会话控制。只读审核员无需获得 Telegram 授权或主面板密钥，即可审查案件。 仅限聊天的访问权限与 全账户设置及完整日志导出功能相互独立。

自动 MTProxy 会从四个公共来源或 运营商目录中维护可用的 Telegram 路由。[IP 模式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/#ip-modes)决定 在连接失败时是必须等待另一个代理，还是可以使用明确允许的直连路由。 外部 HTTP 请求拥有独立的路由和关闭开关。

## 归档工具

0.7.1 包含[历史数据采集](https://phishdestroy.github.io/TgWitness/zh/docs/reference/history/)、[存档搜索与分析](https://phishdestroy.github.io/TgWitness/zh/docs/reference/analysis/)、[只读 MCP](https://phishdestroy.github.io/TgWitness/zh/docs/reference/mcp/)、[本地 OCR/转录](https://phishdestroy.github.io/TgWitness/zh/docs/reference/media-analysis/)以及[外发 webhook](https://phishdestroy.github.io/TgWitness/zh/docs/reference/webhooks/)功能。分析报告和识别出的文本与 捕获的事件保持分离。

[“案件看板](https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-board/)”可在工作区内添加与来源关联的书签、引文、笔记和 收藏集。[报告生成器](https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-reports/)用于选择 材料、章节以及八种设计模板之一，以支持 HTML/PDF 导出。

## 可选附加功能

日常配置流程为：账户 → 数据源 → 监控。**附加功能**是一个独立的存储目标， 包含一个 Telegram 见证机器人和一个 GitHub 捕获预览功能。每个功能在显示 设置前都会说明其可用性和要求。点击卡片可查看操作指南；此操作不会注册或启动任何服务。

机器人设置分为三个步骤：创建只读访问权限、选择发布设置，以及 在 Witness 主机上启动。网络和发布选项、现有连接以及 验证命令均按需显示。 下载的配置文件与 正在运行的 Witness 实例不同。切换附加功能时会保留草稿；账户变更和锁定 操作将清除临时令牌和表单。内置指南包含启动说明。 [GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)会从您的 分支中启动一个已固定的采集器，捕获一个聊天记录，并生成包含工作流溯源信息的加密交接包。

## 协议及私有来源

**MTProto 是 Telegram 的协议；Telethon 是 TgWitness 用于 与 MTProto 通信的 Python 库。**它们并非替代性的连接方式。“收集”功能使用 MTProto； 可选的“见证”功能则通过 Bot API 发布经过签名的校验记录。

每个工作区都有其专属的授权客户端和账户更新流。TgWitness 从配置好的来源中筛选观察数据，并针对历史快照和媒体下载等功能 分别发出明确的请求。

私有消息源无需公开用户名。Telegram 的对等节点类型和数字 ID 是 其标识符；标题和用户名可能会发生变化。访问权限取决于现有的 成员身份和权限设置。TgWitness 不会自动加入消息源，也不会绕过 加入审批。来自其他账户的访问哈希值并非通用访问令牌。

数据采集模型必须考虑加入群组前的隐藏历史、参与者/管理员 角色、会话撤销、权限移除或变更、群组向超级群组 的迁移、主题/论坛、关联讨论、频道身份以及不可用的 附件。并非所有组合都已在实际环境中经过验证。

在收集器启动时会检查来源可见性。若在限定范围内的 对话结果中缺少某个来源，则表示**访问状态未确认**，而非已证实被删除。一个来源不可用 并不妨碍对其他可访问来源的观察。切勿在公开的测试数据中放置 邀请链接或真实会话。

## 多个账户

该面板支持任意数量**的工作区**，每个工作区均拥有：

- 授权机制、加密存储库及连接路径。
- SQLite日志和Ed25519签名身份。
- 精选来源、媒体队列和捕获设置。
- 监控状态、错误、检查点和导出功能。

切换显示的工作区不会停止另一个采集器的运行。跨工作区的重复账户 授权将被拒绝。已绑定到某个 Telegram 账户的日志无法重新分配给另一个账户；但允许重新连接同一账户。 这可确保账户身份及相关消息 ID 范围的完整性。

该应用程序未设定固定的工作区数量。每个工作区都在 一个共享的 Python 进程和事件循环中运行其自身的采集器 任务，用于连接监控、媒体下载、复核以及新聊天记录的采集。吞吐量取决于工作负载。为 实现进程隔离，请使用独立的安装、端口和数据目录。

为每个账户分配其可访问的来源。不同的账户可能观察同一个 群组，但它们的观察记录保持独立，并保留其来源。同一台由操作员控制的机器上的两个账户 并非两个独立的见证者。**导出群组时，** 会将单独签名的作品空间 ZIP 文件打包，并附带一份签名的文件列表，其中包含其 作品空间 ID、哈希值和签名密钥指纹。 每个日志都保留其自身的 边界。在案件笔记或分析工具中构建跨工作区的综合时间线， 同时保留这些来源引用。

## 捕获与归因

“来源”功能提供按账户设置的新消息、编辑、删除、点赞 及成员资格开关。预设选项可保留所有类别，或仅保留消息/编辑/删除记录。 该策略适用于工作区中选定的群组，重启后仍保持有效，并附有 变更前后的签名。默认设置为保留所有类别。 关闭某类别 不会删除旧记录；重新开启该类别也不会重建已遗漏的事件。 操作记录、其他群组服务事件以及显式历史快照是 独立的。捕获的 Telegram 对象可能会保留嵌入的元数据，无论 “单独更新”开关的设置如何。目前尚不支持按群组覆盖类别设置。

| 资料 | 立即捕获 | 边界 |
| --- | --- | --- |
| 消息 | 文本、同行/消息 ID、发件人元数据、回复及原始更新信封 | 作为由采集器签署的、账户可见的观察记录予以保存 |
| 编辑 | 新观察到的版本及任何先前保存的版本 | 系统停机期间的中间编辑内容可能会丢失；发件人未必就是编辑者 |
| 删除 | 通知及先前捕获的内容（如有） | 通常不包含删除者或精确的操作时间 |
| 账户级删除通知 | 原始通知；已解决的记录包含保存的聊天记录及关联方法 | 要求范围内必须且仅有一个先前保存的私聊或普通群组匹配项；其他 ID 保持为 `deletion.unscoped`。频道和超级群组 ID 不包含在此关联范围内 |
| 反应 | 已交付的计数器及可见的近期身份信息 | 获取完整的可用反应器列表需要单独查询；频道可能会隐藏身份 |
| 会员 | 服务消息及已送达的参与者更新 | 可见性取决于角色和聊天类型；事件缺失并不意味着该事件不存在 |
| 管理员操作 | 频道/超级群聊天导出中包含的相关已交付更新及管理员日志快照 | 导出功能会在导出管理员账户可访问日志时读取日志；持续轮询管理员日志的功能不属于此流程范围 |
| 附件 | 原始版本描述符、下载字节数/SHA-256 及尝试结果 | 已消失的文件可能无法恢复；最新版本不会被替换 |
| 历史 | 当前可见消息的明确快照 | 不会还原所有编辑或已删除的内容 |
| 采集进程 | Start/stop, heartbeat, errors, settings, scope and signed run receipt | Local inventory; GitHub and TDX add [independent environment checks](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope) |

The interface names the account supplied in the source event and retains observed names and usernames. When the event omits its actor, the report leaves that field unspecified.

## 容量与 Telegram 限制

没有一个通用的聊天数量标准能保证监控质量。 监控能力取决于每秒峰值事件数、附件数量和大小、额外的 RPC调用、活跃账户数、磁盘延迟/可用空间、网络状况、Telegram的限制、 可接受的延迟以及队列深度。

Telegram 将被动接收与主动短轮询区分开来。其更新 文档描述了针对公开 频道/超级群组的额外 `updates.getChannelDifference` 调用，并建议**同时进行短轮询的 来源**最多为**十个**。这并非指仅限选择十个群组，也并非完整性保证。

| 模式 | 目的 | 状态 |
| --- | --- | --- |
| 标准说明 | 记录来自选定来源的已发布更新 | 已实现 |
| 优先级复核 | 已标记的来源使用其自身可配置的间隔，并在每次限定范围内的重新检查过程中具有优先级 | 已实现历史记录和消息查询功能 |

优先级星号用于控制这些复查操作。额外的 ``updates.getChannelDifference` ` 短轮询功能不会作为独立的用户模式对外提供。

任意的高频轮询、忽略 FloodWait 或假设额外账户具有线性容量 均非有效的容量规划模型。默认限制为 前 1,000 个列出的对话，每个历史快照最多 500 条消息， 按类型每份收集文件 1–2,000 MiB，以及 4 GiB 未压缩的签名 ZIP 内容；上述 各项均可在**“参数**”中针对每个工作区进行调整。导出操作没有固定的事件数量上限。 浏览器回退模式默认限制为 128 MiB；流式 CLI 具有可配置的 传输限制，默认值为 5 GiB。

## 可靠性和数据恢复

已实现的功能包括 SQLite WAL/同步事务；原子性消息 和媒体任务写入；持久化任务和重试延迟；原始版本描述符； 有限重试；持久化媒体 FloodWait；在文本事件的 网络等待之外下载媒体；在后续写入继续进行时保持前缀稳定的导出；原子设置和 审计记录；登录替换失败后保留有效授权； 受损附加工作区的隔离；显式重连尝试；明确的 授权丢失报告；以及使用单调时钟进行实际时间变化检测。

账户和频道的 pts/qts/seq 会在重启后保存并恢复，且被监视的聊天记录 会定期重新核查；详见[证据格式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#durable-collection-and-process-receipts-02)。定期保存位置 并不构成对日志接受情况的原子性、无损确认。

每次进程启动时，都会记录上一次的头部和离线边界。当前历史记录 不被视为缺口修复。Telegram 的差异保留是有限的； `differenceTooLong` 无法重建所有已消失的内容。不可恢复的缺口必须 保持明确标注，即使后续的历史快照成功生成也是如此。

## 证据模型

每条事件记录包含事件序列、本地 UTC 观测时间、来源时间（如有提供）、 事件类型、来源、操作者（如有提供）、原始有效载荷、前一次哈希值及签名。 消息观测记录还会保留采集器账户/运行上下文。

该签名处理收据包含一个随机运行 ID；TgWitness/Python/OS 的 依赖项版本；源文件的 SHA-256 值及聚合指纹；初始账户、 范围和设置；UTC/单调读数；以及前一个日志头。 设置变更、启动/停止及错误信息均记录在同一日志中。检查点在 启动时、监控期间每五分钟（可调整）以及有序停止时被保留。 保留的本地检查点可检测是否回滚至较早的日志前缀。

| 工作原理 | 其功能说明 |
| --- | --- |
| 文件 SHA-256 | 字节与已知摘要匹配 |
| 事件哈希链 | 记录相对于已知边界的排序/关联 |
| Ed25519 | 使用特定密钥生成的签名 |
| 独立保留的检查点 | 后续内容与保留的边界一致 |
| 程序文件大小 | 收集器关于已测量文件的自我报告 |
| 有效的独立 TSA 响应 | 在明确的信任假设下，特定字节在 TSA 时间点上的存在性 |

已实现 RFC 3161 请求准备和 OpenSSL 响应验证功能。 证据模式还会将检查点哈希值提交至配置好的时间戳服务。 保留并验证相关机构的响应，以建立独立的时间锚点。 参见 [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/timestamp/)。

独立保留检查点，控制对签名密钥的访问权限，保存传输 记录，并使用可信软件验证导出文件。[验证范围](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope) 部分说明了这些检查如何相互补充，以及适用哪些信任假设。

## 导出、部署与移交

一个带签名的 ZIP 文件包含原始的 JSONL、CSV、HTML 文件、保留的附件、哈希值、一个 带签名的清单以及一个便捷验证工具。该文件涵盖一个工作区和一个固定的完整 日志前缀。面板搜索过滤器不会在用户不知情的情况下删除记录。 密钥、 令牌和 Telegram 会话被排除在外；原始记录仍可能包含 个人信息和 Telegram 元数据。

请将 ZIP 摘要、可信指纹、检查点、处理收据和交接 记录分别保存。应使用来自可信安装环境的验证工具，而非仅因可执行代码 出现在被检查的 ZIP 文件中就对其予以信任。

浏览器界面本地部署时无需 Node.js、CDN 或外部字体。一个 操作员令牌即可控制整个安装过程。远程访问需要 HTTPS 或 SSH 隧道。 提供了原生 Python 代码和容器配置文件，部署示例位于 [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 目录下；已执行的平台检查项另行列出。

默认工作区使用数据根目录；额外的工作区使用`profiles/<id>/`。 备份需要停止进程并具备完整的数据/密钥集。证据 ZIP 文件 并非应用程序备份。密钥可使用外部主密钥来访问新的数据 目录；日志/媒体加密由操作员的磁盘/卷提供。 参见 [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/) 和 [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/operations/)。

## 稳定版发布标准

在正式发布之前，需说明：

1. 真实的私人群组、超级群组、论坛和频道，包含成员/管理员角色以及 隐藏/可见的历史记录，包括登录/双因素认证、权限撤销和访问权限丢失。
2. 针对已知操作，对编辑、删除、点赞、成员身份及媒体内容进行受控处理。
3. 进程/主机崩溃、磁盘故障/磁盘空间已满、文件引用过期、FloodWait、 网络中断、文件损坏以及数据库回滚。
4. 支持持续的多账户使用，可控制延迟、队列、内存和磁盘资源，包括 同时处理静默和活跃的消息源。
5. MTProto状态推进与日志接受之间存在中断。
6. 在目标操作系统/容器组合上进行干净安装，并验证备份与恢复功能。
7. 对安全性、签名以及归属/证据主张的独立审查。

[“访问与权限](https://phishdestroy.github.io/TgWitness/zh/docs/reference/access/)”部分描述了范围限定面板的访问权限。0.6 版本支持 [“ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/)”中所述的受限单账户 TData 以及账户文件导入功能。 发布前请审阅 Telegram API 条款。相关研究参考文献和平台 调查结果详见[“RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md)”。
