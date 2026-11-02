# 面板指南

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/

面板的每个界面：聊天、日志、来源、导出、扩展功能、保护模式和代码检查。

[初始设置与配置](https://phishdestroy.github.io/TgWitness/zh/docs/reference/settings/) · [账户](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/) · [导出与验证](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/) · [案例报告](https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-reports/)

各屏幕的功能说明、其向签名日志写入的内容，以及详细 指南的所在位置。面板每次仅显示一个工作区：一个 Telegram 账户及其专属的 来源、日志和签名密钥。侧边栏顶部的选择器用于切换 工作区。地址包含工作区信息（`?ws=…`）；当地址、 选择器与已加载的账户不一致时，所有操作将被阻止。

## 快速入门

“每日”板块位于侧边栏顶部**，“账户** ”位于**“工作区** ”下， 其余内容均位于**“更多工具与设置** ”下。顶部栏中的**“界面级别** ”切换按钮决定显示多少个板块：

| 级别 | 侧边栏中的部分 |
| --- | --- |
| 简单 | 首页、聊天、更新、存档和设置 |
| 标准 | 另见 Case Board、账户和访问权限 |
| 专家 | 此外还有“来源”、“扩展功能”、“咨询存档”、“参数”、“账户”、“系统日志”和“集成”等模块。 |

“简单调用”从“开始”、“日志”和“导出”页面进入，包含“**主页**”、“**更改**”和“**存档**”。 安全级别仅用于隐藏部分内容。隐藏的功能仍会正常运行，服务器会 自行检查每一项权限。安全级别、语言、主题和时区会按 操作员和工作区分别保存；请参阅[设置](https://phishdestroy.github.io/TgWitness/zh/docs/reference/settings/)。

顶部栏还包含：

- **跳转至某部分**（Ctrl+K，或在 Mac 上按 ⌘K）：通过 `#number`。使用方向键移动，按 Enter 键打开，按 Esc 键关闭。
- **通知**：根据日志生成的故障和聊天变更信息。 **“全选已读**”会清零计数器，“**通知规则**”可打开规则设置。 在 [“扩展功能” → “通知”](https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/#notifications) 中可设置将通知发送至 Telegram、Discord 或电子邮件。
- 此工作区的连接指示器。顶部栏下的**“收集器状态”** 将其细分为 Telegram 连接、事件接收、数据源和附件队列。
- **锁定**：关闭当前浏览器中的面板。Collection 仍会在服务器上继续运行。
- 版本号旁边的保护模式；请参阅[保护模式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/#protection-modes)。

演示工作区包含虚构的消息，且绝不会连接到 Telegram。 任何可能更改真实工作区的操作都会被拒绝。

## 从这里开始

选择一项任务。**“导出我的账户**”会下载该账户当前可读取的内容。 **“跟踪调查”会**记录您所选聊天群组中的新消息、 观察到的编辑操作以及删除通知。设置卡片显示了三个步骤：连接账户、 选择来源、开始观察。目标问题会一直显示在此页面，直到您 回答或跳过它。新建工作区则会直接打开[首次设置](https://phishdestroy.github.io/TgWitness/zh/docs/reference/settings/)界面。

## 聊天

已保存的对话，默认仅限查看。

- 可通过名称或 ID 搜索列表。**选择**“添加”或“移除”以管理关注的聊天。 “**打开 Telegram 链接**”功能接受用户名或邀请链接，并将预览保存到 日志中。**“加入/打开并观察**”会先加入该聊天，再将其添加到您的来源中； 打开机器人会将其发送出去 `/start`.
- 聊天头部显示消息计数：**已删除，保留文本**、**在保存前已删除** 和 **重新检查后未找到**。聊天列表和通知采用相同的 定义。已删除的消息显示为红色，并保留其已保存的文本；已编辑的消息 则保留所有已保存的版本。每次删除操作都会显示已知信息：消息被查看的时间、 Telegram 不会报告删除者身份，或者仅收到了删除通知。
- **“加载历史记录**”功能将最近的 100、250 或 500 条消息导入此视图和 日志中。若要加载所有已启用的消息源，请使用[“消息源”→“完整历史记录”](https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/#sources)。
- **“导出聊天”**功能将整个可见聊天记录下载为一个已签名的 `chat.json` 且 `chat.html`文件。多个关联账户可协同完成此任务：每个账户下载其对应的 消息编号范围并对其部分进行签名，而发起 导出的账户则对整个存档进行签名。参见[“导出单个聊天](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md)”。
- **“人员”**列表显示了该聊天中所有保存了消息的用户。人员个人资料默认处于 关闭状态，因为它们涉及第三方个人数据。当某次聊天中 启用该功能时，个人资料会显示姓名和用户名历史、Telegram标记、头像哈希值、活动记录、 谁回复了谁、其他被观察的聊天，以及被提及的钱包、手机号、用户名 和链接。 每项信息都指向其对应的记录。**导出个人资料**会保存一个签名文件， 可选地设置密码ZIP；关闭个人资料会删除该文件。参见 [“人员个人资料](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#people-profiles)”。
- **“保存个人资料”功能现可**记录聊天或机器人个人资料的快照：描述、 成员、邀请链接、机器人命令。

### 只读、发送和密钥

消息上方有两个开关，用于保护账户和读者：

- 打开聊天时**，“只读”模式**处于开启状态。 若要发送消息或点击机器人 按钮，请将其关闭。每次操作时都会提示**“以 @account 身份发送？**”或**“以 @account 身份点击此机器人按钮？**”，这表明聊天成员会看到该操作，且该操作将进入已签名的 日志。**选择“在此聊天中 10 分钟内不再提示**”可暂时跳过该提示。在**“案件证据**”目标中，无论是面板还是 API，发送功能均处于关闭状态。
- **“隐藏机密”功能可**隐藏看似密码、登录码、API 密钥或 哈希值、机器人令牌、会话字符串、私钥、JWT 或支付卡号 （卡号会通过 Luhn 和校验）的内容。**点击“显示”**将揭示一个值；该揭示操作 会被记录在日志中。为该浏览器关闭隐藏功能的操作也会被记录下来。 仅显示内容发生变化：原始记录和所有导出文件均保留完整文本。

## 日志

工作区已签名的所有记录，按时间倒序排列（最新在最前）。

- **“概览”**统计了已观察到的消息、记录的编辑、删除通知以及 选定的来源。
- **事件时间轴**可按事件类型（全部、编辑、删除、点赞、 成员资格、报道范围）、文本内容及来源进行筛选。可回**载较早的事件**页面。
- 打开一条记录可查看其详细信息、哈希值和有效载荷。**该记录的链接**是一个 可直接打开同一记录的地址。此预览中可能包含的机密信息已被屏蔽； 导出文件则保留原始内容。
- 日志为仅追加模式：面板中没有任何操作可以编辑或删除记录。请通过 **“导出”→“验证日志**”或 `python -m tgwitness.verify`；参见 [“导出与验证”部分](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/)。

## 来源

该工作区会记录哪些对话，以及从中保留哪些内容。更改 仅适用于未来的活动；已保存的记录保持不变。

**“刷新聊天列表”**功能会读取该账户的聊天记录和文件夹，但不会下载消息内容。

### 范围

- **该账户记录的内容** ：**选定的聊天** （仅您添加的聊天）， **Telegram 文件夹** （该账户的一个文件夹，包括后续添加到其中的 聊天）或 **完整账户** （所有聊天，以及每个新出现的聊天、群组、私聊或 机器人）。**调查模式** 适用于专用账户：它记录 该账户所见的一切内容、其自身发送的消息和按键操作，并立即保存每个新 聊天的配置文件及先前可见的消息。 [专用账户指南](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) 解释了为何绝不能使用你的主账号。
- **源类型**将文件夹模式和整个账户模式限制为频道、群组、私聊 和机器人。**自有操作**会添加该账户自身的消息、编辑操作以及 回复时的键盘按键记录。
- **当出现新的聊天或机器人时**：保存其资料，并保存最多（根据所选数量） 其最新的可见消息。

限制：秘密聊天内容绝不会被记录到TgWitness中。当TgWitness未 运行时，系统不会进行任何记录；重启后，它仅会补录 Telegram 仍能返回的内容，且 报告中会显示数据缺口。超出聊天列表限制（除非在 “参数”中更改，否则为 1,000 个对话）的聊天，将在其下次变为活跃状态时被添加进来。在 其他应用中点击的内嵌机器人按钮不会被记录；但机器人的回复会被记录下来。

### 涵盖的聊天

可按状态（**已启用**、**已暂停**、**优先级**、**已排除**、**未确认 访问**、**已忽略**）和类型进行筛选，然后对选定项执行操作：启用、暂停、标记或移除 优先级、从范围中排除或删除。状态图标仅显示当前状态；操作 位于每行菜单中，并附有功能说明。 暂停和排除操作需要 确认，批量操作时同样如此。删除来源时需输入其名称，并会删除其人员 个人资料；其保存的记录仍保留在日志中。

若某来源未显示在该账户的聊天列表中，则表示该来源正在**接收更新，但未出现在聊天 列表中**，同时记录仍在持续到达；否则，**访问状态未确认**。**“可用 聊天**”会添加通过**“添加所选**”或**“添加所有匹配项**”操作选中的聊天。

### 完整历史

将每个已启用来源的可用历史记录加载到“聊天”和日志中。 进度在重启后仍会保留；附件遵循您的媒体设置。参见 [来源历史记录](https://phishdestroy.github.io/TgWitness/zh/docs/reference/history/)。

### 记录

- **选择要保留的变更**：新消息、编辑、删除通知、 可见的点赞、加入和退出。预设会更改表单； **“保存记录设置**”会应用该预设。重新启用某类别不会恢复 已错过的事件。
- **在可能的情况下保留媒体文件**：下载单个文件大小不超过指定限值的附件，设置 每种类型的限值范围为 1 至 2,000 MiB，并限制视频时长（以秒为单位，0 表示无限制）。 每次下载尝试都会记录结果。
- **重新检查**：每隔几分钟检查一次优先级聊天，其他聊天则很少检查，因此该账户 不会触发 Telegram 的 FloodWait 限制。设置为 0 可关闭该组。在列表中用星号标记优先级聊天； 每次检查的聊天数量以及聊天之间的暂停时间可在 “参数”中设置。参见[集合](https://phishdestroy.github.io/TgWitness/zh/docs/reference/collection/)。

## 导出功能

**“下载**”用于准备文件；**“构建报告**”用于选择报告的显示样式。

| 内容 | 用途： | 指南 |
| --- | --- | --- |
| 账户导出 | 该账户当前可读取内容的最新快照 | [账户导出](https://phishdestroy.github.io/TgWitness/zh/docs/reference/account-export/) |
| 共享副本 | 一个已完成的账户导出功能的精简版 | [披露声明](https://phishdestroy.github.io/TgWitness/zh/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| 已签名 ZIP | 日志、报告、附件和验证工具，均位于固定的日志边界内 | [导出与验证](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/) |
| HTML、PDF、JSON 报告 | 一份密封的可读报告 | [案例报告](https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-reports/) |
| JSONL、CSV | 带有签名的原始记录；一个支持公式的电子表格 | [导出与验证](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/) |
| 交接摘要 | 仅包含收件人所需的聊天记录、时间段和联系人 | [证据](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#investigation-handoff) |
| 聊天记录导出 | 一个已签名的聊天记录 `chat.json` 以及 `chat.html` | [导出一个聊天记录](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **使用密码对上述下载文件进行加密**（12 个字符或以上）会保存一个 AES-256 ZIP，该文件可由 7-Zip 或 WinRAR 打开。其中的已签名文件保持不变。 密码不会被存储。
- **“已准备的导出”**功能会保留最多 20 个文件（总大小不超过 2 GiB），外加最新的一个文件，以便 重复下载，每个文件都包含其SHA-256。文件的准备并不代表已成功发送。
- 当浏览器拒绝显示保存对话框时，该面板将回退为普通下载。
- **您的签名身份**会显示密钥指纹。**“保存检查点**”和 “下载**已签名的运行收据**”功能可为您提供存储在收集器之外的记录。 “准备**时间戳请求**”会在不联系任何服务的情况下构建一个 RFC 3161 请求。

## 设置、账户和连接

- **设置**：目标、连接、记录内容及界面。请参阅 [首次设置和配置](https://phishdestroy.github.io/TgWitness/zh/docs/reference/settings/)。
- **账户**：每个工作区及其状态、消息源、事件和附件队列。 可通过 **需要关注**、**收集**、**离线或已暂停** 或 **未连接** 进行筛选，暂停或恢复选定操作，批量导入账户文件并管理 群组。参见 [账户](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/)。
- **账户**：登录及该账户的连接路径。直接连接、WireGuard 配置文件、您自己的代理、公共 MTProto 池或 WARP；准备并检查一条路径， 然后将其应用到该账户、一个组或所有账户。参见 [“连接”和“代理](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/)”[部分](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md)。

## 附加功能

可选：只需一个账户和来源即可开始收集。只有您 选择的选项才会打开其设置，系统不会自动连接任何内容。顶部的“ **保护级别**”卡片显示当前的[保护模式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/#protection-modes)。

| 卡片 | 新增功能 | 指南 |
| --- | --- | --- |
| 存储与磁盘空间 | 备份、将旧文件移至您的云端、一份无法被删除的证据副本 | [存储](https://phishdestroy.github.io/TgWitness/zh/docs/reference/storage/) |
| 目标与保护级别 | 针对您的目标及两个量表的建议设置 | [下方](https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/#goal-and-protection-level) |
| 通知 | 问题、已修改的消息和每日摘要；您专属的控制机器人 | [下方](https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/#notifications) |
| 证据与备份 | 时间戳、更多见证人以及加密的异地副本 | [下方](https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/#evidence-and-backups) |
| 服务器全天候运行 | 一个不支持 SSH 的云服务器，可通过控制面板进行创建和删除 | [高可信度](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#from-the-panel) |
| 独立见证者 | 已签名的检查结果将发布到您的 Telegram 频道或 Discord 上 | [Witness](https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/) |
| 代码检查 | 将正在运行的程序与 GitHub 上的公开提交进行比较 | [下方](https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/#code-check) |

### 目标与保护级别

四个问题：

1. **用途是什么？**个人记录、调查，或是案件证据。
2. **您打算监控多少内容？**少量聊天（最多约 50 个）、大量聊天（最多约 500 个）还是整个账户？这将把聊天列表的上限设置为 1,000、3,000 或 20,000。
3. **照片和文件？**仅限文本、照片和短媒体（照片 20 MB，视频 100 MB），或全部（视频和文档各不超过 1 GB）。选择“全部”并包含完整 账户时，还会保留 4 GiB 的可用磁盘空间。
4. **它将在何处运行？**这台电脑，或者一台始终处于运行状态的服务器。

建议列表中列出了独立时间戳、drand 以及 Telegram 的设备列表，每项 均附有一行说明其作用。时间戳可设置为每 60、30 或 10 分钟生成一次，适用于个人 记录、调查或证据；drand 和设备列表需要时间戳。仅需 **应用**以下更改：这些内容、附件策略以及上述两个参数。每次 更改都是一条日志记录，此外 `setup.applied`。通知、站外副本、 服务器、网关DNS、代码校验和见证人作为后续步骤提供，并配有 各自的表单。

两个指标是根据当前设置计算得出的，而非基于目标：

| 规模 | 要点 |
| --- | --- |
| 可信度 | 签名日志 1、时间戳 3、drand 1、设备列表 1、代码校验匹配 1、见证人轮询 1、经过认证的服务器 2、网关 DNS 日志 1 |
| 可靠性 | 常驻服务器 3 个，异地副本 3 个，对象锁定 1 个，问题通知 1 个 |

**最高**阅读量为 80% 或以上，50% **为高**，25% **为中等**，低于此为**基本**。 可靠性目前根据问题 4 的答案中“始终在线”的服务器进行计算， 在检查任何服务器之前。

### 通知

通知通过 Apprise 发送至 Telegram、Discord、Slack、ntfy、电子邮件、Matrix 以及 100 多种其他服务。选择一项服务，填写一两个字段并发送测试消息，或者 直接粘贴 Apprise 地址。

- **问题**：磁盘空间几乎已满、账户已注销、收集、复制或时间戳 错误。在密封服务器上，开放的 SSH 端口或登录行为也会构成问题。
- **变更**：在被监视的聊天中，已删除、已编辑和缺失的消息将按 每次检查一条通知进行汇总（除非在“参数”中更改，否则每分钟检查一次）。
- **已完成的功能**：历史记录、导出和存储副本。
- **每日摘要**将于服务器时间设定的指定时间发送。

通知中包含聊天名称和消息数量。消息摘要默认处于关闭状态；若 开启该功能，消息正文将从本机发送出去。

**您的操作员机器人**是您通过 @BotFather 创建的专属机器人，用于回答 `/status` 并 `/stats`，并可选地 `/pause`, `/resume` 和 `/copy`。仅列出的聊天和 Telegram 用户 ID 可以使用它；对话内容保存在工作区中。如果另一个应用程序已经接收其命令，请使用一个单独的 机器人。请参阅 [通知](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md)和[操作员机器人](https://phishdestroy.github.io/TgWitness/zh/docs/reference/storage/#operator-bot-and-completion-notices)。

### 证据与备份

- **独立时间戳**每隔 5 到 1,440 分钟，仅将每个已签名检查点的 SHA-256 发送至 RFC 3161 权威机构和 OpenTimestamps 日历。**Anchor 目前** 正在运行一个轮次。参见[时间戳](https://phishdestroy.github.io/TgWitness/zh/docs/reference/timestamp/)。
- **更多见证记录**（在被选中前均处于关闭状态）：最新一轮的 drand 轮次、Telegram 的 已登录设备列表（不含 IP 地址），以及 Cloudflare Gateway 记录的服务器 DNS 查询日志。参见[可选记录](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)。
- **加密备份**会将日志、文件、检查点和聊天记录导出到 S3兼容存储（Wasabi、Amazon S3、Backblaze B2、Cloudflare R2、MinIO）。 所有内容都会先在此机器上进行加密。**请下载加密密钥**并将其 单独保存：没有该密钥，备份副本将无法被读取。在“治理”或“合规”模式下启用“对象锁定”功能， 可确保对象在设定的天数内不会被删除。参[见异地备份](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md)。

### 代码检查

检查已安装的程序是否与已发布的版本匹配。

1. 输入一个 GitHub 仓库（官方仓库已预填）以及一个标签、分支或提交。
2. **“Check now**” 通过该工作区的外部请求路由，向 GitHub API 查询 该提交的文件列表。它将每个被测程序文件的 git blob ID 与该提交进行比对。即使在 Windows 环境中检出时换行符已被转换，仍能匹配成功。
3. 结果列表会显示已更改、新增和缺失的文件（每类最多 50 个），并保存为 一份 `source.checked` 日志记录。

结果仅在运行中的程序文件未发生变更时才视为有效： 更新后请重新检查。无需令牌，且仅支持公共仓库； 聊天记录和凭据不会被上传。匹配操作用于识别磁盘上的代码。这并非 硬件认证；有关硬件认证，请参阅 [Phala Cloud](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)。

## 保护模式

版本号旁边的切换器显示所选模式以及 18 层 保护层中有多少层处于激活状态，例如 `🟠 Witnessed 9/18`。在 **“扩展功能”→“保护级别”**中**切换模式**可打开选项。每种模式描述一个目标，并列出 尚缺的内容；记录、签名和保存的设置在所有模式下均保持一致。

| 模式 | 用于 | 新增功能 |
| --- | --- | --- |
| 🟢 简单 | 监视聊天并保留副本 | “聊天”功能用于导出日志和聊天记录；签名操作在后台运行 |
| 🟡 已签名 | 向平台、主机或滥用处理部门提交报告 | 签名存档、日志检查、检查点、交接摘要 |
| 🟠 已见证 | 可能有人声称记录被篡改的情况 | 一个独立见证人发布经签名的日志头 |
| 🔴 符合法庭要求 | 供律师、警方或法院使用的证据 | 时间戳、加密的异地副本、报告中的案件详情 |
| 🟣 GitHub 认证 | 任何人都能验证其软件的记录 | 代码检查与 GitHub Actions 捕获 |
| ⚫ 摩萨德 | 针对资金雄厚的对手展开的高风险案件 | 一个全天候运行的密封服务器、一个隐藏的 IP 地址，以及全部 18 层防护 |

各层结构：每条记录均经过签名并链式连接；带签名的运行收据；通过 SHA-256保存的附件；带签名的检查点；重新检查；问题警报；只读见证访问； 按计划进行的见证检查；RFC 3161 时间戳；OpenTimestamps 证明；经过验证的 最新时间戳；加密的异地副本；报告中的案例详情；匹配代码 检查； Telegram 永远不会看到这台机器的 IP；外部请求通过代理进行；副本上的 对象锁定；一个封存的、包含提供商记录的服务器。处于关闭状态的层设有 **“设置”选项**，点击后会打开其表单。选择较低模式时会要求确认，且 不会删除任何内容。

## 更多工具

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **查询存档**：搜索已保存的观察记录，审查来源，然后决定 是否将其发送给 AI 模型。参见[存档分析和](https://phishdestroy.github.io/TgWitness/zh/docs/reference/analysis/) [本地 OCR 及转录功能](https://phishdestroy.github.io/TgWitness/zh/docs/reference/media-analysis/)。
- **参数**：数据收集的限制与频率、复核、下载、配置文件、 通知和导出。支持按名称搜索，显示 **仅显示已更改的** 中的值，并使用 **恢复默认值…** 将 默认值保存为草稿。**保存参数** 会从下次使用时起应用这些值， 每次更改都会生成一条日志记录。
- **访问权限**：审阅员、分析师和操作员拥有各自独立的令牌，访问范围仅限于选定的 工作区、聊天群组及权限。详见[“访问权限”部分](https://phishdestroy.github.io/TgWitness/zh/docs/reference/access/)。
- **系统日志** ：该进程自启动以来执行的操作（连接、代理变更、 登录、登录失败、设置变更），其中 IP 地址已被隐藏。**“跟随新行** ”功能可将最新一行始终保持在视图中。消息仅保存在日志中。
- **集成**：AI 服务提供商、[只读 MCP](https://phishdestroy.github.io/TgWitness/zh/docs/reference/mcp/) 连接以及 [已签名的 webhook](https://phishdestroy.github.io/TgWitness/zh/docs/reference/webhooks/)。
- **Case Board**：位于证据旁边的团队私有笔记、书签和片段。参见 [Case Board](https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-board/)。
- “导出”中的 **GitHub Actions capture**：从您的分支中捕获的一段聊天记录。参见 [密封捕获](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)。
