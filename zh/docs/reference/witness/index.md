# 独立见证者

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/

运行一个带有独立密钥和机器人的 Witness 实例，将签名后的检查点发布到频道中，并据此验证导出数据。

[导出与验证](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/) · [高可信度](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/) · [面板指南](https://phishdestroy.github.io/TgWitness/zh/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

流程图 · 收集器 → Witness (签名检查点：记录条数 + 头部哈希值); Witness → Witness日志，自有密钥; Witness → Telegram 频道 (通过其自有机器人发布的签名帖子); 证据 ZIP → verify.py; Witness日志，自有密钥 → verify.py; Telegram 频道 → verify.py (Telegram 桌面版导出功能或 t.me/s 页面) · 收集器 · Witness · Witness日志，自有密钥 · Telegram 频道 · 证据 ZIP · verify.py · 签名检查点：记录条数 + · 头部哈希值 · 通过其自有机器人发布的签名帖 · 子 · Telegram 桌面版导出功能或 · t.me/s 页面

**图表转为文本**

1. 收集器 → Witness (签名检查点：记录条数 + 头部哈希值)
2. Witness → Witness日志，自有密钥
3. Witness → Telegram 频道 (通过其自有机器人发布的签名帖子)
4. 证据 ZIP → verify.py
5. Witness日志，自有密钥 → verify.py
6. Telegram 频道 → verify.py (Telegram 桌面版导出功能或 t.me/s 页面)

## TgWitness 能做什么，以及它不能做什么

| 该工具具有 | 该工具从未 |
| --- | --- |
| 一个工作区的只读**见证令牌** | 采集器的 Telegram 会话或 API 凭据 |
| 其专属的 Ed25519 密钥和日志 | 采集器的存储库、签名密钥或面板令牌 |
| 其专属的 Telegram 机器人令牌 | 消息内容：头部包含记录数量和哈希值 |

令牌在**扩展功能 → 独立见证人**中生成，仅显示一次，且仅以 SHA-256的形式存储。它会打开且仅打开一个端点， `GET /api/witness/head`该端点返回一个刚 签署的检查点，以及已签署的无内容集合计数器和运行状态。 它无法打开面板、读取消息内容或更改设置，且 该处不接受面板令牌。可在同一页面撤销令牌。收集器会记录 新见证密钥开始检查的时间（`witness.seen`) 并显示每个令牌的最后一次检查时间； 超过 2.5 个间隔仍未进行检查的见证人将被标记为逾期。

新见证节点在每次投票时都会发送一个随机挑战； 捕获语句会在收集器签名下方重复该挑战。计数器 与确切的检查点绑定，并包含在签名的见证帖中。旧版头部 仍被独立见证节点接受。仅日志增长本身绝不会被计为新消息。

## 其检查和记录的内容

每隔一段时间（默认间隔为 10 分钟），该工具会：

1. 自行获取头部数据（收集器无法推送或跳过该数据）；
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
3. 将其签名记录追加到自身的日志中：`witness.anchor`，状态为 `ok`、 `key_changed`、`rollback`（记录数少于之前）、`fork`（长度相同，但 头部不同）或 `invalid`（响应未通过验证），或者当 收集器未响应时为 `witness.no_response`；
4. 将结果发布到频道，并附带签名，包括“无响应”的情况——只要 TgWitness 正在运行且能够访问 Bot API。发布 ID 会被记录下来（`witness.posted`）， 发布失败的情况也会被记录（`witness.post_failed`）。

一条记录如下所示；最后一行包含经签名的声明：

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## 运行 TgWitness

您需要一个 Telegram 机器人（可通过 @BotFather 创建），一个该机器人担任 管理员的频道，以及一个可从证人处访问的收集器地址——需通过 HTTPS 连接，且位于 私有网络之外（请参阅[部署](https://phishdestroy.github.io/TgWitness/zh/docs/reference/deployment/)部分中的 HTTPS 配置文件）。

在面板中打开**“扩展功能”→“独立见证人”→“配置”**。三个步骤涵盖 只读访问权限、您的频道和间隔时间，然后启动见证人。发布 策略、可选的 HTTP/SOCKS5 代理以及自定义机器人 API 地址位于**“高级设置**”中。该表单 会下载 `witness.json` 时，会附带此工作区的收集器密钥。通过“**将访问文件另存**为”下载新 创建的只读令牌 `witness-token.txt`；将其与在见证主机上 `bot-token.txt`在见证主机上生成的文件一同放置在该 JSON 文件旁边。收集器绝不会接收机器人令牌。 下载操作不会启动服务或发布消息。任何托管项目的见证都不会 被隐式注册。

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

第一个命令在不进行网络请求或生成密钥的情况下检查配置文件和密钥文件。 JSON 中的路径相对于该文件；CLI/环境路径相对于 工作目录。 将见证指纹保留在其主机之外。收集器的 “最后轮询”指示器仅用于确认请求；发布情况由 Proof 报告，或通过 见证日志和频道进行核查。

如果控制面板位于 SSH 隧道之后，请仅通过 单独的 HTTPS 主机名（参考[此 Caddy 示例](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example)）暴露范围限定后的见证端点。 此时，默认工作区使用 `https://witness.example.org`，其他工作区使用 `https://witness.example.org/profiles/ID`。仍需提供令牌；该虚拟主机不会转发控制面板及其 其他 API 路由。

选择 `all` 可获取定期发布的检查点。五分钟的间隔意味着每个工作区每天约有 288 条记录。`changes`/`problems` 会刻意不发布部分检查结果。 MTProxy 用于数据采集器的 Telegram 客户端。Witness HTTP 轮询和 Telegram 的 HTTPS Bot API 分别使用各自的直接/HTTP/SOCKS5 路由（[Bot API](https://core.telegram.org/bots/api)）。

**在收集器旁边，使用 Docker**（同一主机——独立进程和密钥，但 同一操作员）：将值填入 `.env` 并启动配置文件。

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

如需使用已发布的图片，请使用`docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`。

**在他人服务器上**（一个真正的独立见证者）：将代码库复制到该处，将 `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` 以及上述三个值 设置为 `.env`，然后

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

或不使用 Docker：

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### 发布到 Discord

见证人可以选择在 Discord 频道而非 Telegram 上发布内容。在 Discord 中，打开 **“编辑频道”→“集成”→“Webhook**”，创建一个 Webhook 并复制其 URL。在 配置面板中，第 2 步选择**“Discord Webhook · 您的频道**”。在见证人主机上， 将该 URL 保存为 `discord-webhook.txt` 旁边 `witness.json`；该数据绝不会到达 收集器。

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

每个见证者仅有一个发布源：Telegram 频道或 Discord Webhook，二者不可兼得。帖子 均包含相同的签名声明，且无法@任何人。超过 Discord 2,000 个字符的帖子将被一行简短内容替代，并附带完整的校验码作为 `witness-check.txt`。每条帖子的 ID 记录为 `witness.posted`. `verify.py --channel`仅读取 Telegram 频道的导出数据，因此对于 Discord，请保留见证日志：其中包含 每张支票。

### 选项

| 选项 | 环境 | 默认 | 含义 |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | 检查间隔时间，1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | 等待采集器和机器人 API 的时间：5–600 秒 |
| `--post` | `_POST` | `all` | `all`：每项检查；`changes`：新进展或新问题；`problems`：只有问题和未解答的疑问 |
| `--title` | `_TITLE` | `TgWitness witness` | 每个频道帖子的开头语 |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | 将收集器密钥固定，而非直接采信首个答案 |
| `--proxy` | `_PROXY` | 直接 | `socks5://host:port` 或 `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | 机器人 API 地址，例如本地机器人 API 服务器 |
| `--data-dir` | `_DATA` | `witness-data` | Witness 密钥和日志 |
| `--config` | `_CONFIG` | – | 包含上述任意选项的 JSON 文件 |

收集器地址、令牌和频道来自 `--collector`, `--token` 或 `--token-file`, `--bot-token` 或 `--bot-token-file`, `--discord-webhook-file` 以及 `--channel`， 或 `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` 以及 `_CHANNEL`，这可防止“secret”出现在进程列表中。

配置文件中，选项名称使用下划线分隔，并包含`texts`，该代码会替换频道帖子中的 文字：

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts`密钥：`ok`、`key_changed`、`rollback`、`fork`、`invalid`、`no_response`、`collector`、 `records`、`head`。命令行优先于环境变量，环境变量优先于配置文件。 未知选项或文本密钥会触发提示信息并停止记录，而非被忽略。 措辞绝不会影响验证：verify.py会在每次 发布结束时检查签名令牌。 在`--post changes`或`problems`中，未发布的检查仍保留在 见证日志中，而`verify.py`会将其列为“从未发布”；起始记录中注明了 策略名称。每项检查仍会出现在日志中，因此发布次数减少意味着独立的 Telegram发送次数减少，而非检查次数减少。

即使没有频道，Witness 仍会保留其日志。请将见证密钥指纹 (`python -m tgwitness.witness fingerprint`) 保存在其他地方。

## 多个工作区的公开验证页面

`python -m tgwitness.proof` 该工具最多可同时管理 32 个工作区，并提供一个只读 页面，显示每个工作区的最新签名校验结果。每个工作区在 data 文件夹下都有独立的见证密钥和 日志，以及一个固定的收集器密钥；是否向 Telegram 频道 发布内容可由各工作区自行决定。请从 [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example) 开始：

| 字段 | 含义 |
| --- | --- |
| `title` | 页面标题，1–100 个字符 |
| `data_dir` | 与文件相关的 Witness 密钥和日志；默认 `proof-data` |
| `interval`, `timeout` | 检查间隔（分钟，1–1440，默认 5）；等待时间（秒，5–600，默认 20） |
| `workspaces[].id`, `label` | 简短的小写别名和显示名称 |
| `workspaces[].collector` | 收集器地址；其他工作区以 `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | 必填项，每个工作区各不相同 |
| `workspaces[].token_file` | 包含该工作区只读见证令牌的文件 |
| `workspaces[].channel`, `bot_token_file` | 可选操作：将每次检查结果发布到频道中 |
| `workspaces[].proxy`, `bot_api` | 可选路由和机器人 API 地址 |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

第一个命令会在不建立连接的情况下验证文件和令牌文件。 该页面仅响应 GET 和 HEAD 请求：

- `/` 显示所有工作区；若某个工作区在 2.5 个时间间隔内未被检查，则会被标记为过期。
- `/api/proof` 返回的结果与 JSON 相同。
- `/api/proof/<id>` 下载最新的签名声明（`tgwitness-public-proof-v1`)： 见证记录编号和哈希值、状态、固定的收集器密钥、检查点、收集 计数器以及频道发布是否成功，由该工作区的见证密钥签名。
- `/healthz` 当工作区的监控器停止运行时，会返回 503 错误。

为该页面设置独立的主机名，例如 [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example)。为了验证，请导出 工作区的见证日志，并 `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` ，并按 下文所述使用它。

## 验证

在“证人”一侧，导出其日志：

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

随后，无论身处何地，只需使用采集器生成的签名 ZIP 文件，以及从 Telegram Desktop 导出的频道（*“导出聊天记录* → JSON”生成的 `result.json` ）或其公共 `https://t.me/s/…` 页面：

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py`会检查见证日志（链和签名），然后验证**见证者 所见到的每个头部是否都包含在导出的日志中**：该计数处的记录必须具有完全 相同的哈希值。不匹配的头部将导致验证失败——这意味着日志在 见证者查看后被篡改了。 它还会报告导出后被见证的头部、见证人 记录的异常情况、验证失败的响应、导出中存在匹配检查点的 时间段（“从 X 见证至 Y”）以及缺失部分。后续检查点不会延长这些时间段。 结果包含最后一个匹配的记录编号以及后续 未找到匹配检查点的记录数量。仅计入由该导出本身密钥签署的回答：若导出 由见证人从未见过的密钥签署，则报告为未被见证；若未采用`--fingerprint`，其 签署者将保持未固定状态。 使用`--channel`时，每个已签名的帖子必须与见证日志 逐条匹配：已更改的帖子将验证失败，缺失的帖子将被列出。在 提供的Telegram JSON导出文件中，日期属于可编辑的元数据，不属于已签名的见证令牌范围。 匹配令牌并不意味着发布日期已通过认证；结果会明确 报告未执行发布时间验证。

### 要求设置受见证的导出边界

若需进行必须包含经见证的最终记录的交接，请添加 `--require-witness`：

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

这需要独立保留的见证指纹以及与之匹配的检查点， 且该检查点必须位于本次导出的确切末尾。仅覆盖较早前缀的检查点 是不够的。暂停采集，让见证方观察最终状态，并在 进一步写入日志之前进行导出；如果日志发生变化，请保留另一个检查点并 导出该状态。 仅凭后续检查点无法验证较短导出文件的最终哈希值。 当同时提供`--channel`标志时，若声明的帖子缺失或匹配集为空，将导致此 严格检查失败。若未使用该标志，普通完整性检查仍会报告未被见证的 记录，但不会因此拒绝一个除此之外完整的存档。

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.
