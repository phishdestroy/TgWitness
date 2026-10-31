# 证据的运作原理

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/how-it-works/

通过验证者实际使用的精确公式，详细解释了哈希链、签名、检查点和见证人等概念。

TgWitness 保存收集账户所观察到的内容，将这些观察结果 整合到一份经过签名的日志中，并允许其他人使用可信 密钥和先前保留的检查点来验证导出内容。

[本地文档网站](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally)还提供了 位于 `/docs/concepts/` 的交互式示例，以及位于 `/docs/witness/` 的检查点决策探索器。所有示例消息、 计数和延迟均为虚构。链式沙盒中的哈希值是在浏览器中使用 SHA-256 算法计算得出的。没有任何数据会被发送至 Telegram。

## 消息在变；观察在积累

序列图 · Telegram → 收集器: 新消息：10:00 见面; 收集器 → 签名日志: 追加消息.new; Telegram → 收集器: 编辑：11:00 见面; 收集器 → 签名日志: 追加消息.edited; Telegram → 收集器: 删除通知; 收集器 → 签名日志: 追加消息.已删除; 关于签名日志的说明: 原始内容、编辑内容及删除记录均予以保留 · Telegram · 收集器 · 签名日志 · 新消息：10:00 见面 · 追加消息.new · 编辑：11:00 见面 · 追加消息.edited · 删除通知 · 追加消息.已删除 · 原始内容、编辑内容及删除记录均予以保留

**图表转为文本**

1. Telegram → 收集器: 新消息：10:00 见面
2. 收集器 → 签名日志: 追加消息.new
3. Telegram → 收集器: 编辑：11:00 见面
4. 收集器 → 签名日志: 追加消息.edited
5. Telegram → 收集器: 删除通知
6. 收集器 → 签名日志: 追加消息.已删除
7. 关于签名日志的说明: 原始内容、编辑内容及删除记录均予以保留

此简化流程假设 Telegram 已成功发送每条更新，且所选 账户能够查看该更新。操作事件也会被记录在日志中。删除通知 不会提供删除者信息或确切的删除时间。重复发送的 消息被视为独立的记录；日志中不会进行全局重复项过滤。

## 哈希值涵盖的内容

![观察、编码、哈希和签名：每个新事件都包含前一个事件的哈希值。](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

从内到外解读该公式：**C** 将九个字段转换为精确的字节； **SHA-256** 生成其摘要；**hex** 表示该摘要的存储格式。前一个 哈希值已包含在事件中。**unhex** 将存储的哈希值还原为 32 字节，供 Ed25519 进行签名。

[静态链图](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

设 C(ei) 为九个事件字段的标准 UTF-8 JSON 格式。第一个 `previous_hash` 由 64 个零字符组成。后续的每条记录都包含前一条 记录的十六进制哈希值：

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

该签名覆盖了 32 个原始摘要字节。哈希输入包含 `seq`、`observed_at`、`source_at`、`kind`、`chat_id`、`message_id`、`actor_id`、 `payload` 和 `previous_hash` 这 8 个值。对象键按顺序排列；省略空格和 ASCII 转义符；NaN 和无穷大值被排除。请参阅 [确切的编码](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#event-canonicalization)规则。

流程图 · 64个零字符 → 记录 1 / 哈希值 h1; 记录 1 / 哈希值 h1 → 记录 2 包含 h1 / 哈希 h2; 记录 2 包含 h1 / 哈希 h2 → 记录 3 包含 h2 / 哈希 h3; 记录 3 包含 h2 / 哈希 h3 → 签名检查点：计数 3，标题 h3 (保留在其他地方) · 64个零字符 · 记录 1 / 哈希值 h1 · 记录 2 包含 h1 / 哈希h2 · 记录 3 包含 h2 / 哈希h3 · 签名检查点：计数3，标题 h3 · 保留在其他地方

**图表转为文本**

1. 64个零字符 → 记录 1 / 哈希值 h1
2. 记录 1 / 哈希值 h1 → 记录 2 包含 h1 / 哈希 h2
3. 记录 2 包含 h1 / 哈希 h2 → 记录 3 包含 h2 / 哈希 h3
4. 记录 3 包含 h2 / 哈希 h3 → 签名检查点：计数 3，标题 h3 (保留在其他地方)

| 更改为提供的日志 | 检测依据 |
| --- | --- |
| 修改记录 2，同时保留其已保存的哈希值 | 重新计算的事件哈希值不同；其签名不再涵盖已更改的事件 |
| 重建被篡改的记录及其后的每个哈希值 | 原始签名验证失败；受影响边界处保留的检查点也显示不一致 |
| 删除尾部内容，但保留前缀部分不变 | 在给定前缀之后的某个较早保留检查点显示，导出内容过短 |
| 使用另一把密钥对替换后的日志进行重新签名 | 一个独立的可信密钥指纹会拒绝该替换身份 |

![修改已保存的字段会改变其摘要；重新生成哈希值无法恢复原始签名。](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**请在记录 2 上尝试以下逻辑：**将已保存事件中的 `Meet at 11:00` 更改为 `Meet at 12:00`。 其重新计算的哈希值将不再匹配。重新计算后续链 可以修复其链接，但无法使原始签名覆盖新的摘要。 相比之下，被观察到的 Telegram 编辑操作将生成一条新的日志记录。

[静态变更图](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

仅凭哈希链接无法阻止他人重新计算替代链。 信任来源于使用独立可信密钥验证签名，并 与收集器外部保留的参考数据进行比对。

## 早期检查点新增的内容

![保留计数 3 和 h3 标题；在位置 3 处会检查后续导出的 4 条记录。](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**随着日志的增长，引用位置保持不变。**如果检查点显示 “3 条记录，头部 h3”，则包含四条记录的导出文件可以通过匹配第 3 位处的 h3 来通过验证。 其最新头部为 h4，预计会有所不同。仅包含两条记录的导出文件将无法通过验证。

[静态检查点图](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

在验证检查点签名后，需执行以下操作：

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

导出数据可能超出检查点范围，但必须在保留边界处保持一致。 真正的验证器还会检查每个事件的序列、前一个链接、哈希值和 签名。若仅比较最终存储的头部，可能会遗漏被篡改的内部 记录——因为其保存的哈希值并未更新。

## 证人的归属之地

流程图 · 采集器 / 账户会话 / 密钥 A → 只读检查点端点; Witness / 固定收集器密钥 / 自有密钥 B → 独立的签名证人日志; Witness / 固定收集器密钥 / 自有密钥 B → 只读检查点端点 (申请审核); 只读检查点端点 → Witness / 固定收集器密钥 / 自有密钥 B (已签名的回答); Witness / 固定收集器密钥 / 自有密钥 B → 包含带签名的 TGW1 帖子的频道 (机器人 API / 专属令牌) · 主机 A · 主机 B · 采集器 / 账户会话 / 密钥 A · 只读检查点端点 · Witness / 固定收集器密钥 /自有密钥 B · 独立的签名证人日志 · 包含带签名的 TGW1帖子的频道 · 申请审核 · 已签名的回答 · 机器人 API / 专属令牌

**图表转为文本**

1. 采集器 / 账户会话 / 密钥 A → 只读检查点端点
2. Witness / 固定收集器密钥 / 自有密钥 B → 独立的签名证人日志
3. Witness / 固定收集器密钥 / 自有密钥 B → 只读检查点端点 (申请审核)
4. 只读检查点端点 → Witness / 固定收集器密钥 / 自有密钥 B (已签名的回答)
5. Witness / 固定收集器密钥 / 自有密钥 B → 包含带签名的 TGW1 帖子的频道 (机器人 API / 专属令牌)

该见证工具会记录回滚操作、在相同计数下出现的不同头部、密钥变更、 无效答案及缺失的响应。仅凭计数增加并不能证明 所有早期记录均未发生变更；请将导出数据与保留的 检查点进行比对。在另一台主机上部署见证工具可避免受收集器主机故障的影响； 由独立操作员管理则能提供额外的独立性。

该“见证人”对收集器报告的日志状态进行认证。它不会 独立观察所有 Telegram 消息。请参阅[见证人设置](https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/)。

## 针对已知操作的测试交付

请使用受控组、独立的采集账户以及新的标记。有目的地发送、 编辑和删除消息，并在各阶段之间检查捕获情况。在检查结果之前，请明确定义 预期操作及截止条件。

R = |observed∩expected| / |expected| Δ t = treceipt - taction

仅计入与预期操作匹配的情况；重复的收据不会增加 分子。分母必须不为零。缺失的收据不计入 延迟测量。需记录时间不确定性；请使用您自己控制的删除操作时间， 因为 Telegram 无法提供确切的删除时间。 诸如 5/6 (83.3%) 之类的结果描述的是测试操作，而非所有 Telegram 流量的完整性。

## 选择工作流程

[完整的调查流程演示](https://phishdestroy.github.io/TgWitness/zh/docs/reference/investigation/)将围绕一起 涉及频道、群组、机器人和私聊的事件展开：

1. 启用“全账户调查模式”，并清点所有可访问的聊天记录。
2. 获取日志快照、按聊天分列的完整历史记录以及已保存的附件。
3. 保留实时更改以及任何有意的面板交互及其操作记录。
4. 通过引用的记录和用户资料，追踪数字发件人 ID、回复关系、重复收件人和文件 哈希值。
5. 重建包含时间戳和明确时间间隔的跨聊天时间线。
6. 在保持各账户的来源和密钥相互独立的同时，比较其他账户的工作区。
7. 汇总并验证带签名的日志、用户资料及历史数据导出文件，并附上案件备注。

该网站的《`/docs/cases/`指南》包含交互式案件地图及针对 机器人争议、已删除消息和参与者更名等情况的处理方案。案件笔记 和跨工作区分析功能为外部功能；该应用程序不会自动 生成全局调查图或合并的案件档案。

[已完成验证及剩余工作](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/) · [导出与验证](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#investigation-handoff) · [从一个账户开始](https://phishdestroy.github.io/TgWitness/zh/docs/reference/quickstart/)
