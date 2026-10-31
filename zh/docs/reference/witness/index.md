# 独立见证者

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/

运行一个带有独立密钥和机器人的 Witness 实例，将签名后的检查点发布到频道中，并据此验证导出数据。

[俄语版机器人和代理设置指南](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md)。

收集器会对自己的日志进行签名，因此无论谁控制了收集器及其密钥，原则上都可能 重写或截断日志并重新签名。 Witness 使这种 行为变得可检测。它是一个独立的进程——另一个容器，或者更准确地说，是由他人 运行的服务器——每隔几分钟会获取收集器的已签名日志头，用自己的密钥对所 观察到的内容进行签名，将其保存在自己的日志中，并发布到 Telegram 频道上。

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

该令牌在控制面板的“Witness”页面上生成，仅显示一次，且仅以 SHA-256 哈希值形式存储。它仅打开一个端点 `GET /api/witness/head`，该端点返回一个刚 经签名的检查点，以及经过签名的无内容收集计数器和运行状态。 该令牌无法打开控制面板、读取消息内容或更改设置，且 控制面板令牌在此处不被接受。可在同一页面撤销令牌。收集器会记录 新见证密钥开始检查的时间（`witness.seen`），并显示每个令牌的最后一次检查时间； 超过 2.5 个间隔仍未进行检查的见证密钥将被标记为逾期。

新见证节点在每次投票时都会发送一个随机挑战； 捕获语句会在收集器签名下方重复该挑战。计数器 与确切的检查点绑定，并包含在签名的见证帖中。旧版头部 仍被独立见证节点接受。仅日志增长本身绝不会被计为新消息。

## 其检查和记录的内容

每隔一段时间（默认间隔为 10 分钟），该工具会：

1. 自行获取头部数据（收集器无法推送或跳过该数据）；
2. 验证收集器的签名、固定的收集器密钥（`--collector-fingerprint`， 或首个出现的密钥）、一个非递减计数，以及在计数未变时头部未发生变更；
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

打开**“扩展”→“频道中的机器人”→** 在面板中**设置机器人** 。三个步骤涵盖 只读访问权限、您的频道和间隔时间，然后启动见证器。发布 策略、可选的 HTTP/SOCKS5 代理以及自定义机器人 API 地址均位于**“高级设置** ”中。 该表单 将下载包含此工作区固定收集器密钥的 `witness.json` 。通过“**将访问文件** 另存为 `witness-token.txt` ”下载新 创建的只读令牌；将其与在见证主机上生成的 `bot-token.txt` 一起放置在该 JSON 文件旁边。收集器绝不会接收机器人令牌。 下载操作不会启动任何服务，也不会发布任何消息。任何托管项目的见证节点均不会 被隐式注册。

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

收集器地址、令牌和频道来自 `--collector`、`--token` 或 `--token-file`、`--bot-token` 或 `--bot-token-file` 及 `--channel`，或 `_COLLECTOR`、`_TOKEN`、 `_TOKEN_FILE`、`_BOT_TOKEN`、`_BOT_TOKEN_FILE` 和 `_CHANNEL`，这使得机密信息不会出现在 处理列表中。

配置文件中，选项名称使用下划线分隔，并包含`texts`，该代码会替换频道帖子中的 文字：

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts`密钥：`ok`、`key_changed`、`rollback`、`fork`、`invalid`、`no_response`、`collector`、 `records`、`head`。命令行优先于环境变量，环境变量优先于配置文件。 未知选项或文本密钥会触发提示信息并停止记录，而非被忽略。 措辞绝不会影响验证：verify.py会在每次 发布结束时检查签名令牌。 在`--post changes`或`problems`中，未发布的检查仍保留在 见证日志中，而`verify.py`会将其列为“从未发布”；起始记录中注明了 策略名称。每项检查仍会出现在日志中，因此发布次数减少意味着独立的 Telegram发送次数减少，而非检查次数减少。

即使没有频道，Witness 仍会保留其日志。请将见证密钥指纹 (`python -m tgwitness.witness fingerprint`) 保存在其他地方。

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

该标记确保与提供的、置顶的见证记录保持一致。操作员 仍需确认见证记录的独立性，并单独保存其记录。 该标记并不证明消息的真实性、收集的完整性或经独立测量的运行时间。

“见证”功能展示收集器在特定时间点报告的内容，并证明后续导出的数据与之 一致。它并不表明收集器记录了 Telegram 发送的所有内容，也不 表明消息内容属实。由同一操作员在同一台机器上运行的“见证” 其可信度低于由其他人运行的“见证”。

仅凭计数增加无法证明在线“仅追加”的连续性：离线 比对必须将每个保留的前缀哈希与收集器的完整导出数据进行匹配。 Witness 停机和发布失败会导致某些时间段缺乏外部锚点。缺失的 帖子可针对保留的见证日志进行报告；无论是由同一运营商控制的频道还是服务器， 均不属于不可变的第三方存档。
