# 了解证据如何运作

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/concepts/

消息内容可能会发生变化，但您所观察到的记录应始终可核查。

请在下方探索两个小型实验。它们使用虚构的消息，完全在您的浏览器内运行，且绝不会连接到 Telegram。

## 一条消息，三点观察

当 Telegram 发送新消息、编辑通知或删除通知时，采集器会分别追加三条独立的记录。编辑操作不会替换最初的记录，删除通知也不会将其清除。

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

删除通知既不提供可靠的删除时间，也不说明是谁删除了该消息。保持这些值的未知状态，有助于区分“观察”与“猜测”。

## 修改一条记录。追踪哈希值。

每条记录都包含前一条记录的哈希值。其自身的哈希值涵盖了事件字段，包括该链接。一个外部保留的检查点固定了日志的特定长度和起始哈希值。

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

**C** 将九个事件字段序列化为 UTF-8 格式的 JSON：键按顺序排列，无额外空格，不进行 ASCII 转义，且不包含 NaN/无穷大值。该事件的 `previous_hash` 值为 hi−1。显示的 h0 表示 64 个零字符；签名覆盖了 32 个原始摘要字节。

这九个字段分别为 `seq`、`observed_at`、`source_at`、`kind`、`chat_id`、`message_id`、`actor_id`、`payload` 和 `previous_hash`。这是 TgWitness [文档中记载的 JSON 编码格式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#event-canonicalization)；哈希值和签名本身并非哈希输入字段。

保留检查点

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

请验证固定收集器密钥下的检查点签名，然后将其边界与已验证的日志进行比对。后续导出的文件可能包含更多记录，但其内容在较早的检查点处仍须与原日志一致。

## 三个问题，三种不同的核查方式

[01 / 完整性**该记录是否发生了变化？** 使用独立的可信密钥验证哈希值和签名。](https://phishdestroy.github.io/TgWitness/zh/docs/exports/)[02 / 连续性**之前保留了哪些内容？** 将签名导出文件与由独立见证方保存的检查点进行比对。](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)[03 / 交付**这些测试事件是否已到达？** 将受控的发送、编辑和删除操作与每个账户的日志进行比对。](https://phishdestroy.github.io/TgWitness/zh/docs/cases/)

匹配的哈希链可回答完整性问题。它并不能证明 Telegram 消息已完整送达、消息内容的真实性，或提供一个独立可信的观察时间。

[全程追踪从获取账户到整理案件资料包的完整调查](https://phishdestroy.github.io/TgWitness/zh/docs/cases/)过程。
