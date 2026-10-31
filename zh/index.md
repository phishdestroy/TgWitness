# 消息会变。保留您所见的内容。

Canonical page: https://phishdestroy.github.io/TgWitness/zh/

[开源 / v0.7.0](https://phishdestroy.github.io/TgWitness/zh/docs/reference/changelog/)

捕获 Telegram 消息，保留其变更记录，并导出经签名的记录。

[打开演示](https://phishdestroy.github.io/TgWitness/demo/?lang=zh)[安装指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh)

演示中使用的是虚构数据。无需登录 Telegram 账号。

 [通过 GitHub Actions 采集（预览版）](https://phishdestroy.github.io/TgWitness/zh/docs/capture/) [S3 异地备份：设置与恢复](https://phishdestroy.github.io/TgWitness/zh/#s3)

穿越时空的一则消息#0042

Northstar · 研究虚构来源 / 消息 42

1. **观察到的消息：**09:41:02

   简报从 14:00 开始。
2. **编辑记录已保留**09:43:18

   简报从 15:00 开始。

   保留了旧版本
3. **删除通知**10:06:45

   捕获的内容将保存在您的日志中。

三点观察。一段历史。示例

消息虽已消失，但记录的历史依然存在。

## 每一处变更都清晰记录。随时随地触手可及。

通过虚构的演示数据浏览界面。

TgWitness / 已保存的聊天记录您的观察工作区

![以深色主题保存 Telegram 对话记录，并完整保留编辑和已删除消息的上下文信息](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / 已保存的聊天记录 熟悉的对话视图，消息旁会显示已捕获的编辑记录和删除通知。

TgWitness / 日志本地工作区

![包含已观察到的消息、编辑记录、删除通知及覆盖事件的日志](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / 日志 一个可搜索的时间线，记录您的账户所观察到的内容，包括中断情况。

TgWitness / 编辑历史本地工作区

![详细信息抽屉，用于对比消息的原始版本与编辑后的版本](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / 编辑历史记录：在不覆盖先前记录的情况下，比较捕获的不同版本。

TgWitness / 签名导出文件本地工作区

![导出功能支持生成带签名的 ZIP、JSONL、CSV 文件以及离线 HTML 报告](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / 带签名的导出文件 将日志随身携带，附带清单和独立验证器。

01 / 捕获

### 范围由您决定。

可选择特定聊天、Telegram 文件夹或整个账户。每个账户均拥有独立的工作区。

[比较采集模式](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#scope)

02 / 保存

### 变更内容丰富了故事。

已捕获的版本、删除通知和观察缺口将保留在日志中。

[查看事件矩阵](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#events)

03 / 移交

### 一份随行记录。

包含签名 ZIP 文件、完整保留的文件以及离线报告。可选密码保护。

[导出并验证](https://phishdestroy.github.io/TgWitness/zh/docs/exports/)

## 只要更改一个字节，区块链就会告诉你。

每个事件均链接到前一个哈希值，并带有 Ed25519 签名。

![捕获的事件会链接到之前的哈希值，附带签名，并以可验证的导出格式传输。](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![修改已捕获的记录会改变其哈希值，并导致关联记录的验证失效。](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![通过单独保留的检查点，接收方可将导出的日志与之前的记录进行比对。](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

了解每种验证机制的具体作用及其局限性所在。

[探索八个证据等级](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#levels)

## 欢迎其他审阅者提供意见。

将观察记录、文件和离线 HTML 报告整合为一个签名包进行交付。

[阅读证据模型](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/)

tgwitness-evidence.zip带签名的软件包

- 01

  原始观察结果JSONL 记录 + CSV 表格
- 02

  易于理解的背景信息离线 HTML 报告 + 保留的媒体文件
- 03

  独立验证带签名的清单 + 独立验证器

签名通过与可信密钥进行比对来检测篡改行为。它们既不能证明消息源自 Telegram，也不能保证完整捕获。日志内容和媒体文件需要由您提供加密存储。

## S3备份。外部验证。

保留加密副本并添加独立校验机制。

默认处于关闭状态

### 将所有内容复制到兼容 S3 的存储中

日志、文件、带时间戳的检查点和聊天记录导出——在上传至 AWS S3 或兼容存储之前均已加密。

**存储设置与恢复**

客户端加密

`AES-256-GCM`对本机上的对象进行加密。服务提供商接收加密后的对象。

定时或手动备份

立即复制，或选择 1 至 1,440 分钟之间的间隔。在面板中查看进度。

Object Lock

在存储桶支持的情况下，选择保留天数和模式。该面板会报告已上传对象的保留状态是否已确认。

经过验证的恢复

请下载加密密钥并单独保存。在另一台机器上进行恢复；文件仅在验证通过后才会发布。

![完整的异地备份配置面板：端点、区域、存储桶、访问密钥、计划任务、对象锁定及恢复密钥控制](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

展开后显示包含高级选项的完整面板。未显示任何存储凭据。

日志与媒体`AES-256-GCM`兼容 S3 的存储服务

[配置 S3 并恢复副本](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3)[阅读验证详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#off-site-copy-and-restore-s3)

**不具备的能力** 若无导出的解密密钥，该工具无法恢复数据，也无法替代独立见证人。

### 通知 · Apprise

通过 Apprise 接收问题警报、聊天变更和每日摘要：支持即时通讯软件、电子邮件或您自己的 JSON Webhook。

**不执行**：除非您启用了“摘要”功能，否则不会发送消息正文。

 [配置通知接收端](https://phishdestroy.github.io/TgWitness/zh/docs/reference/operations/#notifications)

### 外部时间戳

使用 RFC 3161 和 OpenTimestamps 对时间戳检查点进行哈希计算。

**不具备的能力** 它不会将待处理的日历收据视为已确认的比特币时间戳。

 [查看时间戳证明](https://phishdestroy.github.io/TgWitness/zh/docs/reference/timestamp/)

### 独立见证者

一个独立的主机用于存储已签名的观察记录，并可发布 `TGW1` 检查点。

**不具备的能力** 同一收集器主机上的两个工作区不会被视为独立的见证者。

 [设置见证器](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)

### 数据恢复与可见缺失

重启后可继续操作。重新检查并 `coverage.json` 显示已恢复的消息及缺失部分。

**不具备的能力** 该工具不会还原所有被遗漏的编辑操作或已消失的消息。

 [检查连续性和缺失部分](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#continuity)

## 您的首个工作区从这里开始。

请先体验演示版。准备就绪后，连接专用账户。支持 Windows、Linux、macOS 或 Docker。

[阅读安装指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh)

**一个导入的会话，一个正在运行的客户端。**

请勿在 Telegram Desktop 和 TgWitness 中同时运行同一组导入的 TData/会话密钥。Telegram 可能会使共享授权失效（AUTH_KEY_DUPLICATED）。如需并行使用，请通过手机或二维码创建一个独立的 TgWitness 登录账号。

[请阅读会话导入警告](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh#session-warning)

**连接前请先浏览。**

无需 Telegram 账号，即可体验这个虚构的工作区。

[打开在线演示 →](https://phishdestroy.github.io/TgWitness/demo/?lang=zh)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**本地安装命令**

步骤 01

### 获取源代码。

[下载源代码 ZIP](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) 文件并解压，或克隆代码库：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

运行该程序需要 Python 3.11 或更高版本。如果系统中缺少 Python，Windows 启动程序会提供安装选项。

[浏览版本](https://github.com/phishdestroy/TgWitness/releases)

Windows 上没有 Python？[请下载便携版软件包](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip)，解压后双击 `TgWitness.cmd`。

步骤 02

### 选择运行方式。

双击 `Start.cmd`，或在 PowerShell 中运行：

```
.\Start.cmd
```

只是想了解一下？双击 `scripts\Demo.cmd` 即可体验独立演示。无需登录 Telegram。

在支持 Python 3.11+ 及 `venv` 的环境下：

```
sh start.sh
```

若要打开虚构的日志，请运行 `sh start.sh --demo`。

在已运行 Docker 并安装 Compose 2.20+ 的情况下：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

第二个命令会显示您的私有面板令牌。请将其保存在您的设备上。

启动后，请访问 [127.0.0.1:8787 并输入](http://127.0.0.1:8787)。

对于源代码安装，令牌位于 `data/live/panel-token.txt`。Telegram 登录可使用内置的 API 设置，或使用您在 [my.telegram.org](https://my.telegram.org) 上生成的密钥对。[完整设置指南 ↗](https://phishdestroy.github.io/TgWitness/zh/docs/reference/quickstart/)

**TgWitness 0.7.0** [最新动态 →](https://phishdestroy.github.io/TgWitness/zh/docs/reference/changelog/) · [功能与已知限制 →](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/)

## 清晰的说明。有用的下一步操作。

[浏览指南 ↗](https://phishdestroy.github.io/TgWitness/zh/docs/)

[### 模式、应用场景和证据等级 四种采集模式。八个验证级别。为您的案件找到合适的工作流程。](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html)

[01 ### 连接账户 支持通过手机、二维码及会话导入数据。](https://phishdestroy.github.io/TgWitness/zh/docs/accounts/)[02 ### 选择代理 公开的 MTProxy 列表或您自己的路由。](https://phishdestroy.github.io/TgWitness/zh/docs/proxies/)[03 ### 设置 Witness 机器人 您 Telegram 频道中的签名检查点。](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)[04 ### 导出与验证 分享捕获的历史记录并验证其完整性。](https://phishdestroy.github.io/TgWitness/zh/docs/exports/)

## 查阅存档。

加载历史记录、审查 AI 来源、连接 MCP 客户端、识别已保存的媒体文件并发送带签名的 webhook。

可从当前源获取。0.7.0 便携版预览版早于这些工具发布。

[探索工作流](https://phishdestroy.github.io/TgWitness/zh/docs/archive/)

## 开始之前。

**本页面是否与 Telegram 相关？**

不，这是一个包含虚构示例和截图的静态项目页面。实际应用程序运行在您的计算机或服务器上；登录操作也在那里进行。

**它能恢复在捕获前已被删除的消息吗？**

不。TgWitness 仅保留数据采集运行期间您的账户所观察到的内容。后续的历史快照无法还原未捕获的编辑操作或已删除的消息。

**我的整个日志是否都经过加密？**

账户凭据和签名密钥存储在加密保险库中。本地消息和附件需要存储在加密磁盘或卷中。导出文件可选配密码保护的 AES-256 ZIP 格式。

**该网站与 Telegram 有关联吗？**

不。TgWitness 是一个独立项目，基于 Telethon 构建，并根据 MIT 许可证发布。您可通过内置的 API 设置或您自己的 API 密钥对来授权您的账户。

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## 先探索一下。准备就绪后再进行设置。

[打开演示](https://phishdestroy.github.io/TgWitness/demo/?lang=zh)[安装指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh)
