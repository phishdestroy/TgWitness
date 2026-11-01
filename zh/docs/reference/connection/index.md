# 连接、代理和数据保护

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/

身份验证、自动代理池、IP 模式、备用策略、外部请求及密钥存储。

本文档描述了 TgWitness 0.7.1 的行为及其限制。身份验证、 源访问、网络连接和捕获完整性属于各自独立的状态。 有关登录步骤、文件格式和多账户管理，请先参阅 [“账户与会话格式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/)”部分。有关事件策略和重启 行为，请参阅[“数据采集原理”部分](https://phishdestroy.github.io/TgWitness/zh/docs/reference/collection/)。

## 认证方法

**API ID 和 API 哈希用于标识应用程序；它们不能替代账户登录。** 在 TgWitness 中，它们是可选的。优先级顺序为：表单中输入的一组，然后是来自 导入的账户 JSON 文件中的一组，接着是保存在工作区中的一组，最后是内置的 50 个 对，当Telegram拒绝某组时，系统将按随机顺序尝试并自动轮换。只有 Telegram Desktop密钥对（2040）会随匹配的Telegram Desktop客户端描述一同发送。 您可在[my.telegram.](https://my.telegram.org) org的API开发工具中生成的自有密钥对可用于所有账户；每个账户仍拥有独立的授权。

| 方法 | 要求 | TgWitness 支持 |
| --- | --- | --- |
| 手机号、代码、可选的双因素认证 | 账户访问；API 对（可选） | 面板登录 |
| 认证密钥 HEX + DC ID | 完整的 512 个字符密钥和 DC 1–5 | “直接**授权密钥**”选项卡；在保存授权前，可选的“用户 ID”字段需先进行验证 |
| Telethon StringSession | 一个有效的会话字符串 | 面板登录 |
| Telethon SQLite `.session` | 封闭式、连贯的文案 | 支持直接导入 7/8 版本的模式；可选离线命令行界面 (CLI) |
| Pyrogram SQLite `.session` | 已关闭的生产环境用户会话 | 直接通过面板导入模式 2/3 |
| Telegram 桌面版 TData ZIP | 一个现代账户；若设有保护，则需输入本地密码 | 带校验和/解密校验的内存内转换 |
| 账户 JSON | 支持的 API/会话/密钥字段 | 仅凭元数据即可自动填充 API 凭据；但仍需通过会话/密钥或手机/二维码登录 |
| 二维码登录 | 来自授权 Telegram 应用的确认 | 本地 QR 码生成、过期/重试功能，可选双因素认证 |
| TDLib / Pyrogram StringSession | 其他特定于库的格式 | 不支持 |
| 机器人令牌 | 一个拥有独立访问/更新模型的机器人 | 此收集器未使用该工具 |

Telegram 采用代码发送方式；短信送达无法保证。API 哈希值无法修复 已被撤销的会话，也无法替代遗忘的双因素认证密码。TgWitness 不会将 登录代码或 Telegram 双因素认证密码持久化存储到磁盘中。

对于私密来源，该账户必须已具备访问权限。无需提供群组用户名。 使用代理或会话导入既不会授予成员资格，也不会授予管理员 权限。当前成员身份并不保证能够访问加入群组前的历史记录。

## 导入 Telethon 会话文件

Telethon SQLite、Pyrogram SQLite 和 Telegram Desktop TData 采用不同的格式。 该面板会检测并转换受支持的结构；重命名文件并不属于 转换操作。在**“文件**”下选择一个会话及其对应的 JSON 文件，然后点击**“连接账户**”。最多支持四个匹配文件， 总大小不超过 8 MiB。 有关 TData/JSON 的详细信息，请参阅[格式限制](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/)。 不提供密码恢复功能。通过手机/双因素认证或二维码登录将创建独立的授权。

仅限 Telethon 的可选命令行路径仍然可用：

1. 停止客户端使用原始会话，并制作一份一致的副本。该 转换器会拒绝包含未完成 WAL/日志的文件。请正确关闭原始 客户端，而非通过删除这些文件来绕过检查。
2. 在 TgWitness 环境中，运行：

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. 在**“添加账户”→“文件**”下，加载结果或 粘贴其字符串，然后继续。
2. 请核对显示的数字账户 ID，选择数据源并开始监控。

该转换器以只读模式打开 SQLite，不执行任何模式升级或网络请求， 也不会打印会话内容。它会检查模式版本、表类型、单个 会话行、IP/端口/数据中心以及密钥长度。CLI 输入限制为 64 MiB；StringSession 文本限制为 4 KiB。 面板转换会将文件上传至经过身份验证的 TgWitness 服务器，在内存中进行处理，并将规范化的凭据返回至该 浏览器，且不会保存上传的原始文件。连接远程服务器时请使用 HTTPS。

**转换后的文件是一个未加密的账户访问密钥。** 请将其保存在受保护的 存储位置，切勿将其提交或发送给第三方转换服务。TgWitness 会将其授权会话保存在加密保险库中。复制会话不会 创建单独的授权：请勿使用克隆的授权密钥运行多个客户端， 并假设它们能独立接收更新。

转换操作仅传递授权，而非原始消息、实体缓存或 持久化更新游标。它无法解决进程重启后的更新恢复问题。

## MTProto、Telethon 和代理服务器

MTProto 是 Telegram 的协议。Telethon 是 TgWitness 使用的 Python 客户端库。 MTProxy 是一个 Telegram 传输代理；SOCKS5 和 HTTP CONNECT 提供通用 隧道。这些均无法替代账户身份验证。

请在登录前，通过**“账户 → 设置 → 连接设置 → 更改连接路径**”为每个工作区保存路径。 新工作区默认采用**“自动 MTProxy · 公共列表**”模式，并启用“隐藏 IP”功能。 现有工作区若曾明确使用“直接”模式，将保留支持该模式的设置。

## IP 模式

路由方式决定了连接方式。IP 模式则决定了服务器地址 何时可能被暴露。这些控制功能不会安装 VPN，也不会将设备的所有流量进行路由。

| 模式 | Telegram | 外部请求 |
| --- | --- | --- |
| 隐藏 IP（`hide`） | 请使用代理；若均无法连接，请稍候。无直接备用方案。 | 要求使用 SOCKS5/HTTP；拒绝未通过适用代理的请求。 |
| 允许备用方案（`fallback`） | 自动 MTProxy 可能会在配置的延迟时间过后使用 Direct，随后恢复使用正常工作的代理。 | 建议使用已配置的外部代理或该账户的 SOCKS5/HTTP 路由；否则允许使用“Direct”模式。 |
| Tunnel / VPN (`tunnel`) | 允许使用直连路径，并支持即时自动切换至备用池。 | 若未配置相应的代理服务器，则允许直接连接。 |

隧道/VPN 模式假设您单独管理该网络。如果没有可用的 隧道，目标方可看到服务器本身的地址。请根据 您的实际网络环境选择模式，而非仅依据选项名称。

### 选择路径

| 路径 | 设置 | 边界 |
| --- | --- | --- |
| 自动 MTProxy | 内置列表或运算符目录 | 维护一条可用的 Telegram 路由；直接备用方案取决于 IP 模式 |
| 直接 | 隧道/VPN 模式 | Telethon 使用主机的网络路由 |
| SOCKS5 | 主机、端口、可选的用户名/密码 | python-socks，已启用远程目标 DNS 功能 |
| HTTP CONNECT | 主机、端口、可选的用户名/密码 | 仅支持纯 HTTP CONNECT；尚未实现与代理服务器本身的 TLS 连接 |
| MTProxy | 主机、端口、密钥 | 实验性 Telethon 传输协议；32 位十六进制数字或 `dd` + 32 位十六进制数字 |

虚假 TLS `ee` 密钥将被拒绝。Telethon 1.45 的规范化处理可去除前缀 和域名，但这并不实现虚假 TLS 功能。请粘贴 `tg://proxy?server=…&port=…&secret=…` 或 `https://t.me/proxy?server=…&port=…&secret=…`，并选择**“从链接填充字段**”。 这将在不建立连接或保存的情况下验证并填充字段；请单独审查并保存 路由。手动字段仍可使用。参见 [Telegram 代理链接](https://core.telegram.org/api/links#proxy-links)。

### 由您的安装环境提供的公共代理

内置列表整合了四个来源： [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto)、 [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro)、 [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) 以及 [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector)。 捆绑的快照包含端点信息、来源归属及下载日期。 提供商被列入列表并不证明该代理能够正常工作或能接收 Telegram 的所有更新。

**MTProxy 会自动**检查 Telegram 的传输连接状态，保持代理正常运行， 并在代理失败时切换至其他代理。当有足够的 可用代理条目时，工作区会优先使用不同的代理；无法保证使用唯一的出口地址。 失败的代理 将暂停一段时间后再尝试。如果所有代理均无法使用，则由 IP 模式决定收集 是否必须等待，或可使用直接连接。更换代理不会更改账户 或清除其日志。路由选择和变更均记录在已签名的日志中。

当自动路由处于活动状态时，列表每小时刷新一次，传输检查默认 每十分钟运行一次。这些间隔时间均可配置。**更新公共列表** 会触发刷新；仅查看列表不会更改已保存的手动路由。

每个数据流响应限制为 1 MiB，请求超时为 8 秒， 总下载时限为 20 秒；重定向 请求将被拒绝。每个来源最多保留 64 条兼容条目，并进行去重处理。 解析器支持十六进制和 base64url 格式的密钥，以及 JSON 数据流。 伪造的 TLS `ee`、无效链接、私有/保留的 IP 字面量以及本地主机名将被 跳过。主机名在使用前会进行解析和验证，并为该连接固定所选的 IP 地址。自动重新获取会再次解析主机名；若要再次解析，请重新应用 手动条目。

若数据源响应失败、为空或不兼容，将保留之前的源快照。 更新操作具有原子性，采用序列化处理，且每个工作区每分钟仅限尝试一次。 传输探测成功仅表示已建立连接，并不意味着匿名性或捕获的完整性。

**Telegram 流量和 HTTPS 请求使用不同的路由。**列表下载使用 独立的 HTTPS 连接以及提供的外部请求路由。 `TGWITNESS_PROXY_FEED_PROXY` 会通过 HTTP/SOCKS5 代理显式覆盖该路由； 两种 Compose 收集器变体均会转发该路由。后台池遵循主工作区。 不会向数据源提供商发送任何 Telegram 会话、API 凭据、控制面板令牌或机器人令牌。 提供商名称、快照日期和下载路径会显示在**“列表来源”部分**。

MTProxy 仅传输 Telegram 流量。工作区中的 HTTP 操作（如时间戳、 通知、异地副本和源头验证）在 配置时会使用独立的 SOCKS5/HTTP 代理，随后则使用该账户的 SOCKS5/HTTP 路由。若未配置上述任一设置，Hide IP 将拒绝 该请求；其他模式则允许直接连接。 外部请求可被禁用。明确 配置的订阅源下载代理仍由操作员单独控制。 独立的见证服务保持其自身的路由。

****自动池参数**** 在 **参数 → 自动 MTProxy** 下，配置失败阈值、冷却时间、 计划轮换、代理共享以及允许的备用延迟。 | 控制项 | 默认值 | | --- | --- | | 替换前的断开次数 | 10 分钟内 3 次 | | 每次连接尝试尝试的代理数量 | 3 | | 故障后的首次/最长休息时间 | 10 分钟 / 6 小时 | | 计划轮换 | 已禁用；故障时切换 | | 每个代理的账户数 | 0：优先使用独立条目，需要时共享。设置为 1 则等待独占条目。 | | 允许 Direct 回退前的延迟 | 10 分钟；Hide IP 仍拒绝 Direct | | 数据源刷新 / 传输检查 | 60 / 10 分钟；主工作区设置适用于共享池 | 不同的代理并不保证会使用不同的出口地址。这些设置不会 覆盖 Telegram 的限制，也无法保证匿名性。

若要用您自己的运营商目录替换公共列表，请配置以下覆盖设置。 这将完全禁用外部订阅，包括当其 `proxies` 数组为空时。

[将空目录](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) 复制到 `proxy-config/proxies.json` ，并添加您已部署的公共端点：

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

必须替换示例值。最多接受 32 个不同的条目。 经过身份验证的列表会返回标签/主机/端口，无需共享密钥；选择其中一个 会将其凭据保存到工作区保险库中。在进行 明确的传输测试之前，可用性尚未经过测试。如果目录格式不正确，则可进行手动配置。

本地运行：将 `TGWITNESS_PROXY_CATALOG` 设置为本地 JSON 路径。Docker：

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

该覆盖层以只读方式挂载 `proxy-config`；文件必须可被容器 UID 10001 读取。 该目录被排除在 Git、Docker 构建上下文和源代码归档之外。此 目录用于配置收集账户；[Witness 机器人](https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/)使用其自身的 HTTP/SOCKS5 路由，而非 MTProxy。

直接备用方案由上文所述的 IP 模式决定。在 更改路由前请暂停监控。保存操作将断开旧客户端的连接并取消未完成的登录；新 客户端将使用已保存的路由。该账户的日志/会话绑定关系保持不变。 设置将覆盖之前的路由：编辑时请重新输入代理凭据。

凭据采用`network.enc`加密。API不会返回用户名、 密码或密钥。签名记录包含路由类型以及凭据 是否存在，但不包含端点和密钥。操作员可在控制面板中查看端点。 密钥字段在保存、锁定或切换工作区后将被清空。

**测试 Telegram 连接**（登录前也可使用），通过该路径建立并关闭一个临时 未经授权的 Telegram 连接。该操作不会联系任何 IP 检测 网站。测试成功仅表示传输连接已建立，并不代表群组访问权限、消息 完整送达或匿名性。

该代理适用于 Telegram 客户端的连接，包括 Telegram 数据中心（DC）的媒体 下载。浏览器、pip、SSH 以及手动调用的 TSA 工具则采用独立路径。 代理主机名可在本地解析。`rdns` 影响目标主机名； Telegram 通常提供数据中心（DC）的数值 IP 地址。

SOCKS5 和普通 HTTP CONNECT 本身不会对代理凭据或 客户端到代理的隧道进行加密。MTProto 会单独保护 Telegram 流量。 在不可信网络中，请使用 适当的安全通道连接至代理。私人群组 属于云聊天；MTProto 不会将其转换为端到端加密的“秘密聊天”。

## 加密与签名

| 层级 | 已实现 | 操作员责任 |
| --- | --- | --- |
| Telegram 流量 | Telethon MTProto | 平台可信度、传输路径及可用性 |
| Web 控制面板 | 持有人令牌、默认回环设置、请求限制 | 通过 HTTPS 或 SSH 隧道进行远程访问 |
| 秘密 | Fernet 用于管理 API 凭据、会话、代理凭据及签名私钥 | 保护解密密钥和运行主机 |
| 保险库密钥 | 新安装时使用本地密钥或外部主密钥 | 独立的受保护存储空间和密钥备份 |
| 消息和附件 | 明文应用程序存储 | 加密磁盘/卷 |
| ZIP/JSONL/CSV/HTML | 完整性校验，不进行内容加密 | 保护导出的副本和传输内容 |
| 来源与时间 | 签名日志、流程收据、RFC 3161 工具 | 可信密钥、独立检查点/TSA 及保管流程 |

“账户”中的**存储保护功能**会显示这些状态。面板令牌是一种 访问密钥，而非加密密码。它授予管理员访问权限； [已签发的令牌](https://phishdestroy.github.io/TgWitness/zh/docs/reference/access/)可限定在特定账户和聊天群组范围内。工作区共享 主机进程，并非独立的租户。

一个显式启动的、隔离的合成演示实例可通过直接 回环连接自动打开。此功能使用独立于进程生命周期的机制；既不会 泄露配置的面板令牌，也不会授予对真实工作区的访问权限。远程、 代理或跨源请求均无法获取或使用此自动进入功能。 此便利功能不会消除针对真实账户数据的身份验证边界。

BitLocker、LUKS、FileVault 或受管加密卷可在 各自的威胁模型下保护存储数据。 已解锁且正在运行的机器的管理员 仍然可以读取数据。在存储规划中应将 SQLite WAL/SHM、媒体文件、临时导出文件、交换文件、备份 以及浏览器下载内容纳入考虑范围。Docker 卷仅因其 是卷这一事实，并不意味着它已被加密。TgWitness 不实现 SQLCipher 或对象加密。

## 外部主密钥

对于新安装，请将主密钥放置在数据目录之外。 此操作不会自动迁移现有的本地密钥库。请准备一个 仅服务身份可访问的密钥目录，然后运行：

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell，使用已安装的项目环境：

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

在 Docker 中，将文件以只读方式挂载到 `/data` 之外（例如 `/run/secrets/tgwitness-master.key`），并将环境变量设置为该路径。 该服务的 UID 必须具备读取权限。请通过 环境/配置文件传递路径，而非密钥字节。

每个工作区都会获得一个随机的公共盐值，以及通过 HKDF-SHA256 派生出的专属 Fernet 密钥。`vault.external.json` 仅存储派生元数据，而非主密钥。 若密钥缺失或错误，系统将无法启动，且不会在后台自动替换密钥。请同时保留 盐值元数据和主密钥以备恢复之用。

所有工作区均源自同一主密钥；若主密钥遭泄露，将影响整个 安装环境。运行中的进程可解密机密信息。本工具并非硬件安全模块（HSM）或 密码密钥派生函数（KDF）。不接受使用任意人工设置的密码代替随机密钥。

在有计划的迁移 实施并验证之前，请保留现有安装中的现有密钥。删除 `vault.key` 或替换主密钥可能会导致 无法访问会话/签名密钥。请将加密备份与密钥分开存放，并 在隔离的环境中测试恢复功能。

## 来源与验证范围

2026年10月26日审核：

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0：SQLiteSession、StringSession、`Connection._proxy_connect`、 `TcpMTProxy.normalize_secret` 及下载方法。

本地测试涵盖回环 SOCKS5/HTTP CONNECT 测试用例、合成 SQLite 会话、 路由隔离、密钥排除以及密钥缺失时的拒绝处理。这些测试并未验证 真实的 Telegram/代理互操作性或 MTProxy 的实际运行行为。请参阅 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/) 和 [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)。
