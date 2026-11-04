# 跨所有聊天记录进行调查

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/cases/

一个横跨频道、群组、私聊和机器人的完整案件：采集、串联线索、重建时间线、移交。

一个虚构事件，从头到尾。采集、搜索和人员档案找到记录，[Case Board](https://phishdestroy.github.io/TgWitness/zh/docs/case-board/) 整理它们，[Report studio](https://phishdestroy.github.io/TgWitness/zh/docs/reports/) 呈现它们。

已处理案例 / 支付目的地变更

### 一起事件。四段对话。一条需要还原的线索。

一条频道帖子指向一个机器人。一个群组在讨论新的付款链接，机器人也显示了它。帖子被编辑，私聊中重复了该链接，一条群消息消失了。

每个版本是由谁发布的？该链接出现在哪里？哪个文件被保留下来了？有哪些变化，以及何时发生的？

历史加载、AI、MCP、OCR 和 webhook：[使用存档](https://phishdestroy.github.io/TgWitness/zh/docs/archive/)。

## 1. 确保覆盖整个账户

整个账户范围仅用于专用账户。主账户只用选定的聊天或一个文件夹。

1. 在独立工作区中[连接账户](https://phishdestroy.github.io/TgWitness/zh/docs/accounts/)。记下案件编号、账户 ID、工作区和密钥指纹。
2. **来源 → 观察范围 → 调查模式**：**整个账户**、全部四种来源类型、**自身操作**。每个新聊天都会保存其资料和最近 **200 条可见消息**。点击**保存范围**并确认。
3. **加载聊天**并与账户的聊天列表比较。上限为 1,000 个对话（在**参数 → 从账户列表读取的聊天**中最多可设为 20,000）；超出上限的聊天在变得活跃后才会出现。
4. **记录设置** → **所有可见活动**，检查附件限制和磁盘空间。启动后，用一条消息、一次编辑和一次删除进行测试。

频道群组私聊机器人

一个账户 / 一把签名密钥**所有选定的、账户可见的活动 → 整合为一本日志**

消息 · 编辑 · 删除通知 · 可见反应 · 成员活动 · 自身操作

“整个账户”指该账户能打开的每个聊天，减去排除项。不含私密聊天。新聊天出现时即加入；旧历史不会自动下载。

## 2. 获取历史记录并保存文件

创建一个 Case Board 集合，为重要内容添加书签。维护一份来源登记表：聊天 ID、标题、账户、角色、实时捕获开始时间、历史结果、媒体结果、空缺。

| 需求 | 面板中的操作 | 功能介绍 |
| --- | --- | --- |
| 已启用聊天记录的历史 | 来源 → 加载完整历史记录 | 可用的历史消息将进入工作区日志，支持暂停/恢复功能，并生成带签名的进度报告。[历史记录指南](https://phishdestroy.github.io/TgWitness/zh/docs/reference/history/)。 |
| 日志中的现有聊天记录 | 来源 → 记录设置 → 历史快照 | 最近的消息作为签名记录。默认 500 条，在**参数 → 最大历史快照**中最多可设为 10,000。 |
| 某次聊天的当前可见完整历史记录 | 导出完整聊天记录 → 导出完整聊天记录，或 聊天 → 导出聊天记录 | 每个聊天一个独立的签名包，包含 `chat.json` 和 `chat.html`。 |
| 新聊天出现时的上下文 | 监控范围 → 当出现新的聊天或机器人时 | 它的资料和最多 1,000 条最近消息（调查模式下为 200 条）。不适用于已有的聊天。 |
| 附件字节数 | 下载可见附件 + 各类附件的限制 | 查找带 SHA-256 和大小的 `media.saved`。排队中、已跳过或失败都表示未保存。 |

聊天导出不会进入日志或人员档案。要在 TgWitness 内搜索旧历史，请使用**加载完整历史记录**或快照。

这里是：频道、群组、机器人聊天和私聊，以及发票文件及其哈希。捕获前已删除的内容已经没有了。

## 3. 记录不断发展的对话以及您自身的行动

保持运行。将热点聊天加星标作为优先，在**记录设置 → 重新检查**中调整重新检查，并留意 `recheck.completed`、FloodWait 和媒体结果。

**聊天 → 个人资料 → 立即保存个人资料**会保存聊天的简介、机器人命令和其他元数据。

**作为案件调查的一部分，关注机器人或接受邀请**

1. **聊天 → 打开 Telegram 链接**，先保存预览。链接和预览会成为签名记录。
2. 如有需要，**加入 / 打开并观察**会加入聊天或用启动参数启动机器人。
3. 要记录某个操作，请在面板中回复或使用**按下按钮**。您会得到 `interaction.requested` 和 `interaction.result` 以及机器人的回答。

这些是真实操作。在其他应用中按下的按钮不可见，只能看到机器人的回复。不支持网页应用、付款或电话/位置。

## 4. 追踪聊天记录中的人员、链接和文件

1. **日志**、**所有来源**，搜索短语、域名或用户名。打开结果并**添加到案板**。
2. **聊天 → 联系人 → 开启个人资料**，选择一个人：名称历史、回复、活动、**还出现在……**、链接、钱包、电话。打开被引用的记录。
3. 在其他聊天中追踪同一个数字用户 ID。相同的名字、钱包或头像只是线索，不是证据。
4. 比较文件哈希。SHA-256 相同 = 字节相同。是谁分享的则是另一个问题。

案例地图 / 追踪引用虚构案例 · 非实时图表

频道 / 公告**原文 → 编辑后的目标文本**

记录 #101、#188 消息 #84 · 未标注发件人

组 / 运营**用户 71001 发布了新链接**

记录 #146 · 消息 #309 已保存文件收据 #151

机器人 / 订单对话**一个按钮指向该目标页面**

记录 #173 · 消息 #12 “返回”按钮的元数据

私密 / 后续**用户 71001 重复了收件人信息**

记录 #205 · 消息 #922 已保存文件收据 #209

四个聊天记录提供了不同的观察结果。请追踪每条连接的源记录；该频道帖子未标注发件人。

本操作指南中的数字 ID 和记录引用均为虚构。此说明图展示了如何将搜索结果、个人资料和已检查记录相互关联；“案件看板”存储相应的卡片和来源引用。

| 连接 | 辅助观察 | 保留结论 |
| --- | --- | --- |
| 同一 Telegram 账号 | 用户 ID 71001 所在的群组 #146 和私聊 #205 | 两个聊天中的发送者 ID 相同。这个人现实中是谁是另一个问题。 |
| 重复的目标 | `pay.example.invalid/new` 在 #146，按钮元数据 #173，编辑后的帖子 #188 和 #205 | 同一个链接出现在四个地方。谁控制它需要其他来源。 |
| 相同文件字节数 | 已完成的媒体收据 #151 和 #209 中 SHA-256 值完全一致 | 两个文件逐字节相同。 |

档案只包含在*此工作区*中发过言的人，不是成员列表。每个事实的引用数：**参数 → 每个事实引用的记录**。

## 5. 还原事件序列并标注缺失部分

先在**聊天**中查看版本，再到**日志**中选择**所有来源** + **编辑**、**删除**、**覆盖**。时间线中写上两个时间：Telegram 的日期和被观察到的时间。

1. 09:00 · #101**捕获的频道帖子**

   保留了原始目标。
2. 09:12 · #146 / #151**群组提供了一个不同的链接**

   用户 71001 发布了该内容；附件下载已完成。
3. 09:16 · #173**机器人显示相同的目标地址**

   保存的键盘元数据中包含该链接。
4. 09:20 · #188**频道公告变更**

   原始内容和编辑后的内容均予以保留。
5. 09:24 · #205 / #209**私下跟进时再次强调这一点**

   保存的附件与 #151 具有相同的完整 SHA-256 值。
6. 09:28 · #231**群组删除通知已发送**

   先前的观察结果依然成立：既未提供删除者信息，也未提供确切的删除时间。

示例性的观察时间及参考信息。其他日志记录发生在这些条目之间。

日志顺序是到达顺序，不一定是发生顺序。请将实时记录、快照、恢复的消息、删除和“重新检查时缺失”分开，并将每个空缺标记为未知。

## 6. 将此案例扩展至其他收集账户

每个账户一个工作区，步骤相同。记下每个账户的角色和指纹。消息编号按账户计算，所以务必注明是哪个工作区和聊天。

[账户组](https://phishdestroy.github.io/TgWitness/zh/docs/groups/)显示状态、共享设置并一起导出所有账户，每个账户仍有自己的日志和密钥。跨账户时间线需要您在笔记中自己整理。

案件周期很长？请添加[独立见证人](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)，并测试每个账户实际能捕获什么。

## 7. 提交可核查的案件资料包

每个工作区的签名 ZIP（始终是完整日志，筛选不影响），以及人员档案、聊天导出和文件。

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

请单独发送指纹。每份都对照它自己的工作区验证：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

将验证工具的输出、原件、覆盖范围和移交记录与您的发现放在一起。在 Report studio 中撰写报告。如果接收方需要的更少，请制作[精简移交](https://phishdestroy.github.io/TgWitness/zh/docs/handover/)。
