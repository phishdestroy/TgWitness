# 命令行

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/cli/

支持通过脚本和代理进行搜索、阅读上下文、统计活动以及导出已保存的消息，提供 --json 输出格式、稳定的退出代码以及作用域限定的只读令牌。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文档](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Archive integrations](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

[只读 MCP](https://phishdestroy.github.io/TgWitness/zh/docs/reference/mcp/) · [全文搜索](https://phishdestroy.github.io/TgWitness/zh/docs/reference/search/) · [维基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**预览。** `tgwitness search`, `context`, `messages`, `stats` 以及 `export` 读取 已保存的观察记录，供脚本和 AI 代理使用。它们无法向 Telegram 发送任何内容、更改设置或修改签名日志。

其中 `--json`，标准输出（stdout）将输出且仅输出一个 JSON 文档（`export` 写入 JSON Lines）。 进度、提示和错误信息输出到 stderr。退出代码保持稳定：

| 代码 | 含义 |
| --- | --- |
| `0` | 成功，包括空结果 |
| `1` | 失败：无法访问面板、数据无法读取、导出中断 |
| `2` | 使用错误或请求无效：日期格式错误、未知选项、搜索索引不匹配 |
| `3` | 当前不可用：工作区已在运行中的面板中打开，或者面板提示稍后重试（速率限制、超时） |
| `4` | 访问被拒绝：令牌缺失、过期或已被撤销；聊天超出其范围；或该工具不允许此操作 |

## 两种阅读方式

**通过控制面板（`--url`）。**该命令使用与 MCP 相同的范围限定存档 API。**在“集成”→“MCP”中**建立连接：选择工作区和聊天群组、 工具及有效期，然后复制一次令牌。该连接为只读模式，仅限于 所选聊天群组，每分钟请求次数限制为 60 次，且可随时撤销或 轮换。控制面板登录令牌和 Telegram 凭据在此处无效。

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

远程面板需要 HTTPS；仅在以下情况下才接受明文 HTTP： `127.0.0.1`, `localhost` 和 `::1`。代理环境变量将被忽略，且不接受重定向， 因此令牌仅会发送到您指定的地址。

**直接从已停止的工作区（`--data-dir`）**读取**。**以 完全本地访问权限读取数据目录，无需令牌。请在数据目录的副本上使用，或在 数据收集已停止时使用。签名记录绝不会被更改；与控制面板类似，打开 工作区可能会使其派生索引更新至最新状态。当控制面板已打开该工作区时，该命令将以 代码 `3`；请改通过面板进行读取。若未指定 `--data-dir`, `TGWITNESS_DATA`, `./data/live` 或未指定，则使用运行该命令的安装环境的数据目录。

`--workspace ID` 选择工作区（默认 `default`). `tgwitness messages
--workspaces` 列出您可以阅读的工作区。

## 命令

| 命令 | 结果 |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | 按最匹配结果优先排序，包括词形变体、加引号的精确短语、域名以及 `@username` （[语法](https://phishdestroy.github.io/TgWitness/zh/docs/reference/search/#search-syntax)） |
| `tgwitness search QUERY --exact [--before SEQ]` | 精确文本，按时间倒序排列（最新内容在前），不包含索引 |
| `tgwitness context CHAT_ID MESSAGE_ID` | 前后各十条消息 ID 范围内的已保存消息 |
| `tgwitness messages` | 可阅读的聊天记录 |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | 聊天记录中的已保存消息，按时间倒序排列（最新消息在前） |
| `tgwitness messages CHAT_ID --message ID` | 每条消息的每个保存版本及删除记录 |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | 活动统计数据如下： |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | 将观察记录按日志顺序以 JSON Lines 格式保存 |

日期格式为 `2026-10-01` （UTC 午夜）或带时区的 ISO 时间， `2026-10-01T09:00+03:00`。关于 `search`, `messages` 和 `export` ，它们表示 观察时间。每页最多显示50条记录：请遵循 `next_offset` (`--offset`)进行 排序搜索， `next_before` (`--before`) 其他内容。

Ranked search stops at 1,000 results. The final page may be shorter than `--limit`; narrow the query, chat or period when more matching observations exist.

每条消息结果都包含 `untrusted_content: true`工作区、聊天和 消息 ID、日志序列号、保存记录的哈希值以及面板链接。编辑、 删除通知和 `missing_on_recheck` 属于独立的记录。某条记录的缺失 并不证明该事件从未发生。

### 活动统计

`stats` 统计特定聊天、特定发送者或范围内所有聊天的已保存观察记录数量：

- 按 UTC 小时和星期几（以周一为首）分类的消息；最繁忙的小时和日期；
- 已编辑、已删除和 `missing_on_recheck` 分享；
- 发件人及其消息数量，以及第一条和最后一条消息的时间；
- 出现频率最高的域名以及 `@handles`，在所有 已保存版本中，每条消息仅计数一次；
- 涵盖范围： `coverage.gap` 记录内容以及（若需访问整个工作区） 未检测到收集器心跳的时段（`collector_liveness`).

该时间段基于**Telegram 报告的消息时间**。小时和星期几的计数可 帮助估算发件人的时区，但不能确定其确切时区。相关数据是根据 请求从日志中计算得出的，不会被存储。当您的访问范围涵盖整个工作区时，每个结果都会标明其 所涵盖的日志头。通过 控制面板浏览五秒后，或 `--timeout` 本地等待秒数（默认30）后，读取操作将停止；此时 `complete` 返回 false，且 `partial` 指代第一个未被读取的记录。在此情况下，仅统计 最新记录。

### 导出

`export` 每条保存的观察记录（新消息、快照、 编辑、恢复的消息、删除通知、 `missing_on_recheck` 及已保存的媒体 记录）生成一个 JSON 对象，并按日志顺序排列。每行与其他结果具有相同的字段，包含 完整文本。若启用 `--output`，文件将以 `.partial` 名称下写入， 仅在面板完成记录后才重命名；若导出过程中断，则不生成 文件，并以代码 `1`. `--output` 绝不会覆盖现有文件。使用 `--output` 和 `--json`，标准输出将显示摘要：记录数、最后的日志 序列号，以及（对于整个工作区访问）日志头。

通过控制面板进行导出需要连接到允许**“导出消息” （仅限命令行）**的服务器；该选项默认未勾选。此文件仅为工作副本，并非证据：如需可验证的 移交，请使用**“导出**”中的签名导出文件，该文件 `python -m tgwitness.verify`会进行验证。

The panel rechecks access before emitting each record, including the completion record. Revoked or expired access leaves an incomplete export. Lazy page reads share the archive worker limit with other queries and have a bounded wait.

## 代理技能

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) 向特工说明如何使用这些命令、如何引用记录以及如何处理 捕获的文本。从 `.agents/skills` 需从代码库检出 该文件。对于 Claude Code，请复制 `tgwitness-cli` 文件夹复制到 `.claude/skills/` 项目中的 或 `~/.claude/skills/`.

## MCP 和命令行

两者均使用相同的连接、范围检查和限制。MCP 的结果限制为 一个 64 KiB 的页面，因此 MCP 不提供批量导出功能；命令行会以流式传输的方式输出数据。 `get_activity_stats` 两项功能均可使用。
