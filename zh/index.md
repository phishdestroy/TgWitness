# 消息会变。保留您所见的内容。

Canonical page: https://phishdestroy.github.io/TgWitness/zh/

[开源 ／ v0.9.1](https://phishdestroy.github.io/TgWitness/zh/docs/reference/changelog/)

Export Telegram chats，preserve their history，and share a signed archive others can verify．

[打开演示](https://phishdestroy.github.io/TgWitness/demo/?lang=zh)[安装指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh)

虚构数据，无需登录 Telegram。

 [Export an account or selected chats](https://phishdestroy.github.io/TgWitness/zh/docs/reference/account-export/) [通过 GitHub Actions 采集（预览版）](https://phishdestroy.github.io/TgWitness/zh/docs/capture/) [S3 异地备份：设置与恢复](https://phishdestroy.github.io/TgWitness/zh/#s3)

穿越时空的一则消息＃0042

Northstar · 研究虚构来源 ／ 消息 42

1. **观察到的消息：**09：41：02

   简报从 14：00 开始。
2. **编辑记录已保留**09：43：18

   简报从 15：00 开始。

   保留了旧版本
3. **删除通知**10：06：45

   捕获的内容将保存在您的日志中。

三点观察。一段历史。示例

消息虽已消失，但记录的历史依然存在。

## 每一处变更都清晰记录。随时随地触手可及。

真实界面，虚构数据。

TgWitness ／ 已保存的聊天记录您的观察工作区

![以深色主题保存 Telegram 对话记录，并完整保留编辑和已删除消息的上下文信息](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ 已保存的聊天 看起来就像普通聊天，编辑和删除就显示在消息旁边。

TgWitness ／ 日志本地工作区

![包含已观察到的消息、编辑记录、删除通知及覆盖事件的日志](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ 日志 您的账户看到的一切，可搜索，空缺也会记录。

TgWitness ／ 编辑历史本地工作区

![详细信息抽屉，用于对比消息的原始版本与编辑后的版本](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ 编辑历史 新旧版本并排显示，不会覆盖任何内容。

TgWitness ／ 签名导出文件本地工作区

![导出功能支持生成带签名的 ZIP、JSONL、CSV 文件以及离线 HTML 报告](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ 签名导出 带走日志，已签名，并附带自己的验证工具。

通过[＂案件看板](https://phishdestroy.github.io/TgWitness/zh/docs/case-board/)＂、[报告设计](https://phishdestroy.github.io/TgWitness/zh/docs/reports/)和[共享副本](https://phishdestroy.github.io/TgWitness/zh/docs/handover/)追踪已保存的记录。集中[审查账户组](https://phishdestroy.github.io/TgWitness/zh/docs/groups/)。

01 ／ 捕获

### 范围由您决定。

几个聊天、一个文件夹或整个账户。每个账户都有自己的工作区。

[比较采集模式](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#scope)

02 ／ 保存

### 变更内容丰富了故事。

版本、删除和空缺都保留在日志中。

[查看事件矩阵](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#events)

03 ／ 移交

### 一份随行记录。

签名 ZIP、文件和离线报告。密码可选。

[导出并验证](https://phishdestroy.github.io/TgWitness/zh/docs/exports/)

## 只要更改一个字节，
验证机制就会立即提示。

每个事件均链接到前一个哈希值，并带有 Ed25519 签名。

![捕获的事件会链接到之前的哈希值，附带签名，并以可验证的导出格式传输。](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![修改已捕获的记录会改变其哈希值，并导致关联记录的验证失效。](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![通过单独保留的检查点，接收方可将导出的日志与之前的记录进行比对。](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

请遵循从文件哈希值到单独保留的检查点的验证流程。

[探索八个证据等级](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#levels)

## 欢迎其他审阅者提供意见。

消息、文件和离线报告打包在一个签名包中。

[阅读证据模型](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/)

tgwitness-evidence.zip带签名的软件包

- 01

  原始观察结果JSONL 记录 ＋ CSV 表格
- 02

  易于理解的背景信息离线 HTML 报告 ＋ 保留的媒体文件
- 03

  独立验证带签名的清单 ＋ 独立验证器

接收方用您的密钥核查所有内容，而保存在别处的检查点表明此后没有任何内容被改写。[检查的工作原理。](https://phishdestroy.github.io/TgWitness/zh/docs/concepts/#layers)

## S3备份。外部验证。

保留加密副本并添加独立校验机制。

默认处于关闭状态

### 将所有内容复制到兼容 S3 的存储中

日志、文件、检查点和聊天导出，在发送到 S3 之前加密。

**存储设置与恢复**

客户端加密

在您的机器上使用 `AES-256-GCM`。服务商只能看到密文。

定时或手动备份

立即复制，或每 1 至 1，440 分钟复制一次，进度显示在面板中。

Object Lock

选择保留天数和模式，面板会检查设置是否真正生效。

经过验证的恢复

请单独保存密钥。可在任何地方恢复，文件仅在验证通过后才会输出。

![完整的异地备份配置面板：端点、区域、存储桶、访问密钥、计划任务、对象锁定及恢复密钥控制](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

展开后显示包含高级选项的完整面板。未显示任何存储凭据。

日志与媒体`AES-256-GCM`兼容 S3 的存储服务

[配置 S3 并恢复副本](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3)[阅读验证详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#off-site-copy-and-restore-s3)

**恢复密钥** 请单独保存，没有它副本将无法读取。

### 通知 · Apprise

问题、聊天变化和每日摘要，发送到即时通讯工具、电子邮件或您自己的 webhook。

**选择共享内容** 除非您开启，否则不包含消息文本。

 [配置通知接收端](https://phishdestroy.github.io/TgWitness/zh/docs/reference/operations/#notifications)

### 外部时间戳

使用 RFC 3161 和 OpenTimestamps 对时间戳检查点进行哈希计算。

**跟进结果** 检查 TSA 应答，或将 OpenTimestamps 回执升级为比特币证明。

 [查看时间戳证明](https://phishdestroy.github.io/TgWitness/zh/docs/reference/timestamp/)

### 独立见证者

一个独立的主机用于存储已签名的观察记录，并可发布 `TGW1` 检查点。

**分离参照** 在另一台主机上运行，使用独立的密钥和日志。

 [设置见证器](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)

### 数据恢复与可见缺失

重启后可继续操作。重新检查并 `coverage.json` 显示已恢复的消息及缺失部分。

**查看时间区间** 恢复的消息和记录的空缺并排显示。

 [检查连续性和缺失部分](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#continuity)

## 您的首个工作区从这里开始。

先试用演示，准备好后再连接备用账户。
Windows、Linux、macOS 或 Docker。

[阅读安装指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh)

**一个导入的会话，一个正在运行的客户端。**

请勿在 Telegram Desktop 和 TgWitness 中同时运行导入的 TData 或会话，Telegram 可能会让两者都失效（AUTH_KEY_DUPLICATED）。两者都需要？请通过手机号或二维码单独登录 TgWitness。

[请阅读会话导入警告](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh#session-warning)

**连接前请先浏览。**

无需 Telegram 账号，即可体验这个虚构的工作区。

[打开在线演示 →](https://phishdestroy.github.io/TgWitness/demo/?lang=zh)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**本地安装命令**

步骤 01

### 获取源代码。

[下载源代码 ZIP](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) 文件并解压，或克隆代码库：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

需要 Python 3.11+。在 Windows 上，启动器会提示为您安装。

[浏览版本](https://github.com/phishdestroy/TgWitness/releases)

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

源码安装时，令牌位于 `data/live/panel-token.txt`。您自己的 API 凭据（来自 [my.telegram.org](https://my.telegram.org)）是可选的。[完整安装指南 ↗](https://phishdestroy.github.io/TgWitness/zh/docs/reference/quickstart/)

**TgWitness 0.9.1** [最新动态 →](https://phishdestroy.github.io/TgWitness/zh/docs/reference/changelog/) · [功能与已知限制 →](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/)

## 清晰的说明。有用的下一步操作。

[浏览指南 ↗](https://phishdestroy.github.io/TgWitness/zh/docs/)

[### 模式、应用场景和证据等级 四种采集模式。八个验证级别。为您的案件找到合适的工作流程。](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html)

[01 ### 连接账户 支持通过手机、二维码及会话导入数据。](https://phishdestroy.github.io/TgWitness/zh/docs/accounts/)[02 ### 选择代理 公开的 MTProxy 列表或您自己的路由。](https://phishdestroy.github.io/TgWitness/zh/docs/proxies/)[03 ### 设置 Witness 机器人 您 Telegram 频道中的签名检查点。](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)[04 ### 导出与验证 分享捕获的历史记录并验证其完整性。](https://phishdestroy.github.io/TgWitness/zh/docs/exports/)

## 查阅存档。

历史记录、带来源的 AI、MCP、OCR 和签名 webhook。

[探索工作流](https://phishdestroy.github.io/TgWitness/zh/docs/archive/)

## 开始之前。

**本页面是否与 Telegram 相关？**

不需要。这是一个带虚构示例的静态页面。应用运行在您自己的机器上，您在那里登录。

**它能恢复在捕获前已被删除的消息吗？**

不能。它只保存运行期间您的账户看到的内容。之后的快照无法重建错过的编辑或已删除的消息。

**我的整个日志是否都经过加密？**

会话和密钥是加密的。消息和文件不是，请使用磁盘加密。导出可以设置 AES－256 密码。

**该网站与 Telegram 有关联吗？**

不是。这是一个基于 Telethon 构建、采用 MIT 许可的独立项目。您使用自己的账户登录。

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## 先探索一下。准备就绪后再进行设置。

[打开演示](https://phishdestroy.github.io/TgWitness/demo/?lang=zh)[安装指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh)
