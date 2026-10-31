# 外发 webhook

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/webhooks/

将带 HMAC 签名的指定范围事件发送至 HTTPS 接收端，支持重试并提供投递状态。

**当前主要版本：**请使用源代码检出；0.7.0 便携版预览版尚未包含此功能。

[工作流指南](https://phishdestroy.github.io/TgWitness/docs/archive/) · [维基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

在所选工作区中打开**“集成”→“外发 webhook”**。 添加一个 HTTPS 接收器，选择收集器/媒体/导出事件，并可选地为 新观察项和变更选择聊天。消息正文默认处于关闭状态。启用摘要 功能后，消息变更事件最多增加 1,000 个字符；Telegram 的原始字段和 凭据绝不会被发送。

将 HMAC 密钥复制一次到接收器的受保护配置中。该密钥 存储在 TgWitness 的保险库中并经过加密，无法通过控制面板检索。删除 并重新创建目标以实现密钥轮换。**向合成**测试队列**发送**一条 不含聊天内容的测试消息；刷新投递状态以查看结果。

该功能在 Apprise 的基础上扩展了现有的通知循环。它利用 工作区的外部路由和现有的私有目标限制。 后续不会进行直接的备用处理或重定向。URL 不得包含凭据、 查询字符串或片段；私有地址需要服务器级别的网络 授权，而非面板用户可绕过的设置。

## 有效载荷与签名

模式：[`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json)。每个有效载荷 包含 `event_id`、`timestamp`、`workspace`、`type`、`synthetic` 以及计数器。 基于日志的事件包含其序列号和哈希值。完整导出完成和 合成测试属于交付事件，不包含虚构的签名日志引用。 Telegram 删除通知和 `missing_on_recheck` 仍为独立类型。

`X-TgWitness-Signature` 标头应为 `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`。 使用显示的密钥（作为 UTF-8 字节）对精确字节序列 `timestamp + "." + raw_request_body` 计算 HMAC， 并在解析或处理正文之前以常数时间比较签名。若时间戳与 本地时间相差超过五分钟，则予以拒绝。每次投递尝试时，时间戳都会刷新。

在持久化存储中使用 `event_id` 作为幂等键，并在产生副作用之前设置原子性唯一 约束。仅凭有效的签名并不能防止 最近的请求被重放。请至少在整个 重试窗口内保留已处理的 ID；如果接收方可以重新处理存储的事件，则应更长时间地保留这些 ID。

## 重试

消息发送会在 HTTP 请求之前被持久化地排入队列。该系统采用“至少一次” 语义：若确认消息丢失或系统重启，可能会再次发送具有 相同 ID 的事件。系统会进行八次尝试，采用指数退避机制，起始间隔为 15 秒，上限为一小时。成功发送需返回 2xx 状态码。 已耗尽的任务 会留下可见的错误信息；重试结束后，无法保证能成功交付。

队列可容纳 1,000 次发送任务。当队列已满时，日志事件的扫描将暂停， 并在有可用空间后恢复。 无法排入队列的完整导出任务 会触发可见的队列错误。每次通知处理 最多尝试发送五次，并保留最近 100 条尝试记录。删除一个目标 也会一并删除其待发送的任务。

## n8n 示例

导入[示例工作流](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json)。该工作流处于非活动状态， 且不包含任何机密信息或下游操作。 在 n8n 工作进程环境中设置 `TGWITNESS_WEBHOOK_SECRET`， 允许该环境访问，并为 Code 节点启用 `crypto` 内置函数。该示例使用 Webhook 节点的 raw-body 选项， 检查签名/新鲜度，并确认已验证的事件。这与 该节点的[文档中所述的实现](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts)方式一致。

在添加 SIEM 写入或通知之前，请先添加以 `event_id` 为键值的持久化幂等存储。 根据您选择发送的数据，限制 n8n 工作流的编辑及执行日志的保留时长。 TgWitness 不添加任何入站命令。
