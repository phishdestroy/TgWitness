# 了解证据如何运作

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/concepts/

消息会变。您对所见内容的记录不应改变，而且任何人都应能核查这一点。

下面是两个小实验。消息是虚构的，一切都在您的浏览器中运行，不会发送到 Telegram。

## 从聊天记录导出到可验证的记录

[Telegram Desktop 导出](https://telegram.org/blog/export-and-more)将当前可见的历史保存为 HTML 或 JSON。TgWitness 增加了持续的变更日志、每条记录的签名，以及他人可以对照的检查点。

| 任务 | Telegram Desktop 导出 | TgWitness |
| --- | --- | --- |
| 阅读已保存的对话 | HTML 或 JSON 格式，含选定媒体文件 | 已保存的聊天记录、可搜索的日志和离线报告 |
| 跟踪随时间的变化 | 导出时可用的历史记录 | 旧版本、后续编辑和删除，全部保留 |
| 移交后检查文件 | 标准的 HTML/JSON 导出文件未签名 | 签名清单、签名记录和封印报告，用可信密钥核查 |
| 与先前保留的状态进行比较 | 请保留一份单独的参考副本或哈希值 | 已签名的检查点、独立的见证文件以及可选的外部时间戳 |

本对比基于截至 2026 年 11 月 2 日的 [Telegram Desktop 导出代码](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output)。

## 一条消息，三点观察

一条新消息、一次编辑和一次删除会变成三条独立的记录。编辑不会覆盖第一条，删除也不会抹掉它。

01 / 消息流转示例流程

Telegram delivers an update to the collector, which appends a journal record. · Telegram · 收集器 · 日志 · 更新 → · 追加 →

当前聊天视图 消息 #42

消息已删除

该消息已从聊天界面中消失。

观察日志 3 条记录

1. 01

   `message.new`

   10:00 见面

   ✓
2. 02

   `message.edited`

   11:00 见面

   ✓
3. 03

   `message.deleted`

   关于 #42 的删除通知

   ✓

所有三条已接收的记录均保留在日志中。

针对已选定来源的简化路径。操作记录也会同步到真实的日志中。捕获内容取决于该账户的可见范围以及 Telegram 实际发送的内容。

Telegram 不会告诉您是谁删除了消息，也不会告诉确切时间。TgWitness 将这些字段留空，而不是去猜测。

## 修改一条记录。追踪哈希值。

每条记录都包含前一条记录的哈希。保存在别处的检查点固定了日志长度和最后一个哈希。

02 / HASH-CHAIN SANDBOX真实的 SHA-256 · 记录示例

记录 01**消息已收到**`h₁ = SHA-256(e₁)`链接至 64 个零

记录 02**11:00 见面**`h₂ = SHA-256(e₂)`包含 h₁

记录 03**观察到删除操作**`h₃ = SHA-256(e₃)`包含 h₂

保留在其他地方**3 条记录 · 头部 `h₃`**请将此固定边界与提供的日志进行对比。

修改某条事件会改变其哈希值。重建链条会改变其头部。移除尾部会使其长度短于保留的检查点。

**查看记录 2 及完整哈希值**

这是本示例中经过哈希处理的精确 UTF-8 JSON 数据。数值均为虚构；其中的九个字段及序列化格式均与日志格式一致。

```

```

已保存记录 2 的哈希值

``

重新计算的记录 2 哈希值

``

此沙盒仅计算哈希值，不生成签名。真正的验证器还会检查每个事件的 Ed25519 签名、序列号和链接。仅凭哈希值的重建无法在受信任密钥下生成有效的签名。

## 实际规则，简要概述如下

哈希值 + 签名

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** 是以 UTF-8 JSON 表示的九个事件字段：键已排序，无多余空白，无 ASCII 转义，无 NaN/无穷大。`previous_hash` 是 hi−1，h0 是 64 个零，签名覆盖 32 字节的原始摘要。

字段：`seq`、`observed_at`、`source_at`、`kind`、`chat_id`、`message_id`、`actor_id`、`payload`、`previous_hash`。完整规范：[事件编码](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#event-canonicalization)。

保留检查点

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

用固定的密钥检查检查点签名，然后将其与日志比较。之后的导出可以更长，但在检查点处必须一致。

## 三个问题，三种不同的核查方式

[01 / 完整性**该记录是否发生了变化？** 用您信任的密钥核查哈希和签名。](https://phishdestroy.github.io/TgWitness/zh/docs/exports/)[02 / 连续性**之前保留了哪些内容？** 将导出与见证人保存的检查点比较。](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)[03 / 交付**这些测试事件是否已到达？** 发送、编辑和删除测试消息，看看每个账户捕获了什么。](https://phishdestroy.github.io/TgWitness/zh/docs/cases/)

签名回答“是否被改过”，检查点回答“是否与之前的一致”，测试消息回答“我们是否捕获了全部”。[验证能证明什么、不能证明什么。](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope)

下一步：从开始到案件包的[整个账户调查](https://phishdestroy.github.io/TgWitness/zh/docs/cases/)。

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
