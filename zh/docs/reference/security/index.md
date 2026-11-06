# 安全与数据处理

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/security/

威胁模型、访问模型、静态机密、网络暴露、会话导入以及如何报告漏洞。

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| 领域 | 简而言之 |
| --- | --- |
| 访问 | 管理员密钥加上对账户/聊天的范围限定访问权限，包含七项权限及可撤销的会话；默认使用 localhost |
| 静态数据中的秘密 | 会话、API 对、签名密钥和代理设置均采用 Fernet 算法进行加密 |
| 消息和媒体文件 | 数据以明文形式存储：请使用磁盘加密并设置严格的权限 |
| 完整性 | 每条记录均带有 SHA-256 哈希链和 Ed25519 签名 |
| 本地信任边界 | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

有关漏洞报告，请参阅[安全政策](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)。

## 访问模式

主面板令牌授予完全控制权。其他用户可获得各自的 [范围限定访问权限](https://phishdestroy.github.io/TgWitness/zh/docs/reference/access/)：指定的工作区和聊天群组、权限、有效期、 IP 限制、登录限制以及可撤销的会话。仅限聊天群组的访问权限 即使勾选了相关权限，也无法执行整个工作区的操作。 工作区共享同一进程，其数据不会与主机管理员的数据隔离。

该面板默认监听 localhost。通过浏览器登录会将访问 令牌兑换为会话凭证；浏览器将其作为承载令牌发送。该凭证存储 在 sessionStorage 中，而非身份验证 Cookie 中。锁定/注销会清除 浏览器会话。关闭浏览器或结束会话不会停止数据收集。

已签发的令牌和会话凭据以哈希值的形式保存在加密保险库中。 撤销操作将终止相关会话；权限变更将影响后续 请求。已下载的文件无法被召回。管理员也可以限制其 自身的浏览器会话，但直接使用主面板令牌的脚本仍可保留 完全访问权限，并绕过这些浏览器会话限制。

身份验证失败将根据客户端地址进行速率限制。IP 限制基于 应用程序所识别的地址；在依赖该机制之前，请先检查 反向代理的行为。Witness 凭据仍为独立的只读检查点/健康状态凭据。

### 演示访问

`/api/demo-access` 是一个经过刻意设计的、无需身份验证的引导程序，用于明确 启动的、隔离的合成演示。它仅颁发一个独立于进程生命周期的权限， 绝不会颁发真实的面板令牌或 TGWITNESS_TOKEN 覆盖令牌。 其签发和使用需要 一个回环对等方和主机，不允许转发标头，也不允许跨源请求。额外的 工作区或授权会话将禁用此路径。实时工作区绝不会签发 该权限。该演示无法关联账户或更改收集设置。

## 面板内容与导出功能

该面板不使用任何外部字体、分析工具、CDN资源或嵌入的远程媒体。 来自Telegram的文本以纯文本形式插入，而非HTML格式。下载的附件以 二进制附件形式提供。JSONL导出保留原始字符串；HTML导出则对 这些字符串进行转义；可能包含公式的CSV单元格会在前面添加一个撇号。

导出文件不包含身份验证和签名密钥，但会刻意保留 收集到的源元数据、标识符，以及可能包含的个人或敏感内容。 原始源元数据中可能包含 Telegram 访问哈希值和文件引用。

## 静态数据中的秘密

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### 外部主密钥

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/) for setup details.

## 代理服务器与网络路由

代理配置在保险库中经过加密存储。密码和 MTProxy 密钥 不会通过 API 返回，也不会写入证据记录。每个工作区可自行选择 Telegram 路由和 [IP 模式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/#ip-modes)。

**“隐藏地址”模式会**拒绝直接使用 Telegram 备用连接，并要求通过代理处理外部 HTTP 请求。“显式选择的备用模式”允许在延迟后直接访问 Telegram； “隧道/VPN 模式”则允许直接连接。选择“隧道” 模式不会安装或验证 VPN。这些设置不会控制所有设备 流量、浏览器、软件包管理器或本地代理主机的 DNS 解析。

MTProxy 仅传输 Telegram 流量。外部请求可使用独立的 SOCKS5/HTTP 代理、工作区的 SOCKS5/HTTP 路由，或允许的直连路由； 也可将其禁用。独立见证器拥有自己的传输设置。 普通 SOCKS5/HTTP CONNECT 身份验证不会由这些代理 协议本身进行加密。伪 TLS MTProxy 密钥目前仍不支持。

## 登录与会话导入

转换后的 .tgwitness-session 文件在 加载并存储到保险库之前，其中包含明文授权密钥。离线命令行界面支持经过审核的 Telethon 模式。 面板导入功能还支持 Pyrogram SQLite、现代单账户 TData ZIP 以及文档中记载的 JSON 输入格式。该功能需经过身份验证，限制为 4 个文件 / 8 MiB， 并在内存中处理上传内容，无需解压归档或保存原始文件。 规范化的凭据仅返回给请求的已认证浏览器； 在 Telegram 授权成功后，这些凭据将保存在加密保险库中。 请保护原始文件和转换后的文件，并避免多个客户端同时克隆同一授权。

数据处理过程会验证容器校验和、本地解密哈希值以及结构 长度。系统会临时使用用户提供的 Desktop 本地密码，且不会将其存储。 此有限解析器无法保证所有 Desktop 版本均兼容。 QR 图像在本地生成，包含短效的 Telegram 登录令牌，且 绝不会发送至外部渲染服务。锁屏、切换工作区、新登录 以及路由变更都会取消待处理的 QR 尝试。刷新或关闭标签页可能会导致 尝试处于待处理状态直至过期。成功的 QR 登录仍会强制执行账户绑定。 普通 API 请求主体仍限制为 16 KiB；经过身份验证的导入路径接受 最多 12 MiB 的编码 JSON，并单独执行较小的解码文件大小限制。

登录码和 Telegram 两步验证密码不会被持久化存储。手机号码/验证码哈希状态在 授权过程中仅保存在内存中。Telegram 会话授予账户访问权限；切勿 将数据目录、会话、令牌、保险库密钥或私有签名密钥上传至 GitHub。

## 日志与传输

默认的 API 验证响应已被替换，因此不会回显凭据 值。应用程序访问日志功能已禁用。请勿配置反向代理 以记录 Authorization 头或请求正文。HTTP 以明文形式传输令牌和登录 密钥：只要连接离开 localhost，请务必使用 HTTPS 或 SSH 隧道。

## 完整性限制

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/zh/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## 如果您怀疑存在问题

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.
