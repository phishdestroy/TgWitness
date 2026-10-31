# 一个日志。四种收集模式。八个验证级别。

Canonical page: https://phishdestroy.github.io/TgWitness/zh/guides/modes.html

模式、场景和证据级别

TgWitness 记录已连接账户所观察到的内容。第三方可借助独立的可信密钥验证该记录的完整性。

[收集模式](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#scope)[应用场景](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#scenarios)[证据等级](https://phishdestroy.github.io/TgWitness/zh/guides/modes.html#levels)

3–5 分钟概述 · 虚构示例 · 当前实现

1. **Telegram**

   账户可见的更新
2. **收集器**

   关联记录，每条均已签名
3. **验证者**

   可信密钥 + 保留边界

`h₁ → h₂ → h₃ · Ed25519`已验证完整性。Telegram 的来源与消息的真实性仍是两个独立的问题。

## 选择观察范围

三个观察范围和一个调查预设。排除项和已启用的源类型仍然适用。

默认**选定聊天**

记录

仅采用人工精选的来源。

新聊天

不会自动添加。

选择

一组已知的频道或群组。尚未确定固定的聊天容量。

**不具备的能力** 它不会发现其他聊天记录，也不会补全早期的聊天历史。

账户文件夹**Telegram 文件夹**

记录

文件夹包含项和分类，若已配置，则不包括排除项和已归档的聊天。

新聊天

匹配活跃聊天；一小时内的文件夹变更。

选择

分析员已维护一个案件文件夹。请在专用账户上确认数据收集情况。

**不具备的能力** 它不应用文件夹的动态 muted/read 条件。

确认范围**完整账户**

记录

选定类型中，账户可见的聊天，包括私人对话和机器人。

新聊天

将在首次更新时添加。

选择

一个专门的观察账户，包括参与案件的账户。

**不具备的能力** 它不会自动加入聊天群组，也不会绕过源访问。

整个账户预设**调查模式**

记录

所有源类型、自身操作、源配置文件以及新发现源的最新 200 条可见消息。

新聊天

新的聊天或机器人将获得一个配置文件和历史记录快照。

选择

通过控制面板加入团队或与机器人交互。查看并保存预设。

**不具备的能力** 它不会对所有现有聊天进行快照，也不会观察在其他客户端中触发的回调。

这些卡片仅用于本地比较，并非实时收集器控制项。它们不会更改任何账户。

**不具备的能力** 任何模式均不得读取秘密聊天内容、在进程停止时进行记录、自行加入消息源，或检索超出请求范围的早期历史记录 snapshot/export.

[阅读详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/collection/)

## 通过 GitHub Actions 采集（预览版）

新建 Telegram 登录会话、一个聊天、加密归档和 GitHub 来源证明。

[打开采集助手](https://phishdestroy.github.io/TgWitness/zh/docs/capture/)

## 记录内容

仅已交付或明确请求的观察记录才会被纳入记录。来源不明的观察记录仍保持未知状态。

 捕获开关 · 本地示意图新消息编辑删除内容反馈成员资格

该面板按工作区应用这些开关。关闭某项开关会保留现有记录；重新开启该开关不会重建遗漏的事件。

**事件矩阵：已保存的材料与剩余未知项**

| 分类 | 已保存 | 仍未知 |
| --- | --- | --- |
| 消息 | 文本、ID、发送者元数据、回复上下文及原始更新信封。 | 不存在可由第三方验证的 Telegram 签名。 |
| 编辑 | 记录所有被观察到的版本，且不覆盖较早的版本。 | 中间编辑可能被遗漏；发送者不一定是编辑者。 |
| 删除 | 如有，请附上通知及先前保存的文本。 | 未提供删除者及确切操作时间。 |
| 无作用域的删除 | 账户级通知；未知对等方仍被明确标识。 | 不进行聊天内容推测。关联操作在可能的情况下使用先前保存的账户范围内的 ID。 |
| 反应 | 已交付的计数器及可见的近期身份信息。 | 并非所有反应器都是可见的；获取完整的可用列表需要单独查询。 |
| 成员资格 | 已发送的服务消息和参与者更新。 | 角色和聊天类型限制了可见性；沉默并不意味着不存在。 |
| 附件 | 原始版本描述符、已保存字节、 SHA-256 以及尝试结果。 | 已消失的文件可能无法获取；新版本不会取代它。 |
| 历史快照 | 当前可见的消息，被标记为历史观察记录。 | 早前的编辑记录和已消失的内容不会被重建。 |
| 自主行动 | 发送 messages/edits 及匹配的回复键盘 button_press 元数据。 | 在其他 Telegram 客户端中触发的回调不可见。 |
| 机器人按钮 | 回调、URL、Web 应用及请求元数据将随消息一并保留。 | URL 和 phone/location 请求均为文本，不会被自动打开或执行。 |

### 默认附件限制

照片

20 MiB

视频

100 MiB

文件

50 MiB

动画

20 MiB

视频笔记

50 MiB

语音

20 MiB

音频

50 MiB

贴纸

5 MiB

**不具备的能力** 开关不会屏蔽嵌入的元数据，也不会禁用操作记录。捕获操作不会识别 Telegram 未提供的行为主体。

[阅读详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/collection/)

## 仅使用您拥有的授权权限

每个账户都有自己的工作区、日志、签名密钥、路由和队列。

### 电话号码 + 代码

启用 2FA 。

### QR 代码

请从授权设备进行扫描； 2FA 可能仍需执行此操作。

### Telethon .session

导入该账户的会话文件。

### Pyrogram .session

导入支持的 Pyrogram 会话格式。

### TData ZIP

仅支持一个 Desktop 账户；若已设置，则使用本地通行码。

### StringSession text

粘贴一个 Telethon StringSession.

### .session + .json

选择会话及相应的配套元数据。

### 认证密钥 HEX + DC ID

导入账户授权时需包含其数据中心标识符。

**API pair**

您自己的 API 密钥对是可选的。若未提供， TgWitness 将使用公共密钥对池，其中包括来自官方 Telegram Desktop 的密钥对。

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy 处于实验阶段；内置的公共 MTProxy 列表可用。代理路由失败时不会回退到直接连接。

同一台机器上的两个工作区并不构成两个独立的见证者。

**不具备的能力** 导入操作不会绕过 Telegram 授权， 2FA 也不支持不受支持的会话格式。账户仍共享应用程序进程。

[账户格式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/)

## 从面板操作

发送或回复消息、点击当前机器人按钮、保存链接预览后，请显式加入聊天或使用其启动参数启动机器人。

`interaction.preview``interaction.requested``interaction.result`

预览、请求和结果回执均经过签名。在按下按钮之前，服务器会再次获取消息，并拒绝已更改的键盘输入。返回的回调文本和 URL 仍作为记录上下文保留。

**不具备的能力** 不支持网络应用、支付、 phone/location 分享或内联查询。显示 URL 不会打开该链接。

[阅读详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/collection/)

## 恢复与连续性

应展示缺口，而非隐藏。

### 恢复保存的位置

重启后，系统会向 Telegram 查询遗漏的更新。有限的保留时长和过期的差异可能导致数据缺失。

### 重新检查可见消息

默认设置：优先级来源每15分钟更新一次，其余来源每6小时更新一次。结果包括 message.recovered 以及 message.missing_on_recheck.

### 阅读 coverage.json

观察时段、附有原因的缺失记录以及未观察到的 ID 均随签名导出文件一同提供。重新检查时未发现的记录并不等同于删除通知。

**不具备的能力** 后续的历史快照不会抹去服务中断事件，也无法恢复所有已消失的版本。保存的光标并非对日志接受情况的无损确认。

[阅读详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/)

## 七个层次。不同的问题。

每种机制都针对一个有限的问题提供解答。请单独配置外部服务，并将它们的信任锚点保留在收集器之外。

1. ### 记录

   SHA-256 chain + Ed25519 每个事件；第一个 previous_hash 为64个零。

   **第三方验证** 基于固定收集器密钥的排序和签名。

   **不具备的能力** 这并不证明其源自 Telegram 亦不证明其完整性。

   **验证命令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### 容器

   manifest.json 列出文件哈希值； manifest.sig 对其进行签名。 media.saved 将附件字节绑定到一个事件上。

   **第三方验证** 提供的文件与已签名的清单及媒体收据一致。

   **不具备的能力** 它不会对单独下载的 CSV, HTML 或截图。

   **验证命令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### 保留边界

   启动时进行检查点备份，默认每 5 分钟一次，并有序停止。请在其他位置保留一份副本。

   **第三方验证** 后期的导出结果应与先前保留的长度和头部一致；可检测到回滚情况。

   **不具备的能力** 它无法检测日志和所有保留检查点同时被替换的情况。

   **验证命令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### 外部时间

   证据模式会发送一个检查点 SHA-256 至 RFC 3161 相关机构（FreeTSA, DigiCert) 及 OpenTimestamps 日历。

   **第三方验证** 经过验证的 TSA 响应会标注这些字节的时间戳；已确认的 OpenTimestamps 证明将这些字节锚定至比特币。

   **不具备的能力** 它不会将已准备的请求或待处理的日历收据视为已确认的时间戳。

   **验证命令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### 独立见证人

   将主机、范围限定只读端点、新挑战及其专属 key/journal 以及 TGW1 频道帖子。

   **第三方验证** 先前已接受的分支头；状态包括 ok、 key_changed、回滚、分叉、无效以及 no_response.

   **不具备的能力** 它不会将同一收集器主机上的两个工作区视为独立的见证者。

   **验证命令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### 站外副本

   S3-兼容的副本，使用 AES-256-GCM; Object Lock 加密的副本（当存储桶支持时）。

   **第三方验证** 仅在日志、检查点和已保存媒体的验证成功后，Restore 才会发布文件。

   **不具备的能力** 若未提供导出的密钥，则无法恢复数据；若未检查存储响应，则不假设数据已被保留。

   **验证命令**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### 运行溯源

   签名运行收据：源代码哈希值、依赖项版本及进程上下文。由系统自行报告。

   **第三方验证** 签名收集器对其自身执行情况的报告。

   **不具备的能力** 它不提供独立的进程认证，也不排除记录前已遭入侵的可能性。

   **验证命令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### 任何级别都无法证明的内容

每次 Telegram 更新的送达；文本的真实性；发件人 ID 代表真实个人；记录前收集者未遭入侵；法庭可采纳性。

[独立见证人](https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/)

本地 SHA-256 实验

### 尝试修改第 2 条记录

下一条记录保留了之前保存的链接。修改文本会改变记录 2 的计算哈希值。

记录 2 的正文

记录 1`h1`以 64 个零开头

记录 2`h2`包括已保存的 h1

记录 3`h3`包括已保存的 h2

静态示例： h2 涵盖“11:00见面”。更改该文本会改变 h2；记录 3 仍引用已保存的 h2.

**检查完整的摘要**

已保存记录 2 的哈希值

`SHA-256(e₂)`

重新计算的第 2 条记录哈希值

`SHA-256(e₂)`

此示例计算的是哈希值，而非签名。真正的验证器会使用可信密钥对每个签名和链接进行验证。

 [阅读详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/how-it-works/)

## 选择一条贯穿证据的路径

虚构情境。在相关事件发生前开始收集数据；在记录内容的同时，保留其边界和空白处。

### 频道更改支付详情

模式 → 事件

选定聊天 → 消息、编辑、删除。

输出

通过哈希值记录观察到的帖子版本和附件。

验证

已签名 ZIP + 保留检查点 + 经验证的 TSA 响应。

**不具备的能力** 它无法恢复从未被捕获过的原始数据。

### 事件发生后，消息将消失

模式 → 事件

文件夹或整个账户 → 所有事件类别。

输出

已保存的原始内容、删除通知以及存在缺口的覆盖范围。

验证

已签署 ZIP + 独立见证日志。

**不具备的能力** 若通知中未提供操作主体，则无法据此识别删除者。

### 调查一个商店机器人

模式 → 事件

调查预设 → 按钮、链接预览和显式机器人启动。

输出

已签名的交互收据、返回的回调以及保存的配置文件。

验证

已签名 ZIP；请对照 ZIP.

**不具备的能力** 它不会打开机器人网页应用、进行支付或记录其他客户端的回调。

### 参与者在不同聊天中会更改昵称

模式 → 事件

任何范围 → 被观察的 sender/profile 元数据。

输出

按数字 ID 记录名称/用户名历史、"也出现在"链接及提取的线索。

验证

文件 JSON 已与签名版本核对 ZIP.

**不具备的能力** 它不会将钱包、类似手机号码的字符串或用户名转化为经过验证的身份。

### 长期观察，并保留异地副本

模式 → 事件

任何作用域 → 证据模式以及一个 S3 支持的副本 Object Lock.

输出

加密副本、保留的检查点及时间戳响应。

验证

使用导出的密钥进行恢复，然后在不依赖原始服务器的情况下进行验证。

**不具备的能力** 它不能替代独立见证人或单独保留的解密密钥。

[阅读详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/investigation/)

## 交付可验证的软件包

请提供已签名的原始文件、独立保存的密钥指纹、相关检查点以及验证结果。

- 已签名 ZIP
- JSONL
- CSV
- HTML
- 检查点
- 已读回执
- 聊天记录导出： chat.json / chat.html
- 档案 JSON
- 受密码保护 AES-256 ZIP
- 为多个账户分别导出
- 流式 CLI：5 GiB 默认限制

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

请从可信副本中获取验证器，而非从正在检查的存档中获取。

**不具备的能力** 独立版 CSV 和 HTML 并非签名容器。密码用于保护传输机密性，而非真实性。多次导出不会合并账户日志。

[阅读详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/)

## 对比交付的成果

基本 artifacts 不包含额外的签名、时间戳或见证系统。脚本和日志记录器因实现而异；“部分”指仅限于捕获或可见的内容。

| 方法论 | 编辑 / 删除 | 记录签名 | 外部时间 | 独立见证人 | 覆盖范围 / 缺失部分 | 无作者的验证 |
| --- | --- | --- | --- | --- | --- | --- |
| Telegram Desktop 导出 | 部分 | 无 | 无 | 无 | 无 | 无 |
| Telethon 快照脚本 | 部分 | 无 | 无 | 无 | 无 | 无 |
| 删除日志记录器：文本日志 | 部分 | 无 | 无 | 无 | 无 | 无 |
| 屏幕截图 / 网页截图 | 部分 | 无 | 无 | 无 | 无 | 无 |
| TgWitness 带配置的附加项 | 部分 | 是 | 是 | 是 | 部分 | 是 |

**不具备的能力** 该表格并未评估每一款脚本或日志记录产品。可选的时间和见证人验证需要各自的服务和信任锚点；其中没有任何一项能确立源头真实性。

[阅读详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/)

## 将限制与证据一并保留

当验证范围保持明确时，验证才具有实用价值。

- 秘密聊天功能不可用。
- 进程停止期间不会记录任何内容；恢复能力有限。
- 经过验证的记录并不证明其内容为真。
- 持有密钥的操作员可以对任意内容进行签名。独立见证人和时间戳限制的是后续替换，而非不诚实的初始捕获。
- 请使用专用账户，而非您的主账户。
- Telegram 可能会因请求量过大而限制账户。

**不具备的能力** 任何模式或证据级别均不能确立法律可采性、Telegram消息的完整送达或现实世界中的身份。

[设置指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh)[专用账户](https://phishdestroy.github.io/TgWitness/zh/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/investigation/)
