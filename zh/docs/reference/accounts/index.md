# 账户与会话格式

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/

支持通过手机、二维码或授权密钥登录，可导入 Telethon、Pyrogram 或 Telegram Desktop 的会话数据，并同时管理多个账户。

TgWitness 通过 MTProto 协议以 **Telegram 用户账户**（而非机器人）身份登录，使用 Telethon 实现。每个账户都位于独立的工作区中（在 API 和命令行工具中称为“*工作区*”），并拥有独立的会话、消息源、日志和签名密钥。

会话文件、会话字符串和认证密钥均属于**账户授权凭证**：任何 持有者均可代表该账户进行操作。这些凭证不包含消息历史记录。

> [!警告] **请勿使用任何您无法承受损失的内容。**我们强烈建议不要连接 个人账户或其他重要账户，也不建议在您珍视的账户上 创建 API ID 或 API 哈希。 这并非因为 TgWitness 未经测试：Telegram 会以不可预测的方式限制并 永久封禁账号——仅因其认为请求量 过大，无论使用何种客户端或出于何种目的，且未提供充分的说明文档。许多封禁 都是不可逆的。 请使用专用账号。测试能否顺利进行取决于 Telegram 自身，而非 软件本身，且无法保证后续使用不会出现问题。

- [一览](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#at-a-glance)
- [开始之前：API ID 和 API 哈希值](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [电话号码](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#phone-number) · [二维码](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#qr-code) · [认证密钥 + DC ID](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#auth-key--dc-id)
- [账户文件](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#pyrogram-session) · [会话 + JSON 对](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#telethon-stringsession) · [账户 JSON](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#account-json)
- [识别您拥有的内容](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#identify-what-you-have) · [不受支持的格式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#unsupported-formats)
- [多个账户](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#multiple-accounts) · [确保账户文件的安全](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#keeping-account-files-safe) · [故障排除](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#troubleshooting)

## 一览

| 您拥有 | **“添加账户**”选项卡 | 您还需要 |
| --- | --- | --- |
| 电话号码及其登录码的获取方式 | **电话** | 若已启用双因素认证（2FA），请输入密码 |
| Telegram 在另一台设备上已打开 | **二维码** | 若已启用双因素认证（2FA），请输入密码 |
| `.session`文件（Telethon 或 Pyrogram） | **文件** | 可选的配套 JSON 文件，用于应用程序设置 |
| `.session` + `.json`（同名） | **文件**（请同时选中） | 通常没有其他内容 |
| Telegram Desktop 中的 `tdata` 文件夹 | **文件**（ZIP 压缩包） | 若已设置，则为桌面端本地密码 |
| Telethon StringSession（文本、`.txt`、`.tgwitness-session`） | **文件** | 无需单独的 API 对 |
| 包含会话或认证密钥的 `.json` | **文件** | 无需单独的 API 对 |
| 一个授权密钥（512个十六进制字符）及其DC编号 | **认证密钥** | 可选用户 ID |

TgWitness 根据文件**内容**而非文件名来识别文件。重命名文件 绝不会导致其被转换。

## 开始之前：API ID 和 API 哈希值

您无需创建 Telegram API 应用程序即可登录。当未输入、 未导入或工作区中尚未保存任何密钥对时，TgWitness 会从其内置的 50 组公开 API 密钥对（`tgwitness/api_pool.py`）中按随机顺序选取一组。 如果 Telegram 拒绝某对密钥 （`API_ID_INVALID`、`API_ID_PUBLISHED_FLOOD`、`UPDATE_APP_TO_LOGIN`），则尝试下一对， 每次登录最多尝试八对；被拒绝的密钥对将被跳过，直至重启。用于登录的密钥对将 与该账户一同保存，并供该账户重复使用。**API ID** 和 **API**哈希用于向 Telegram 标识该应用程序；它们 本身并不对账户进行授权。

若要改用您自己的应用程序（注册该应用的账户将面临风险； [参见 “为何要使用内置 API 池？](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)”）：

1. 打开 [my.telegram.org](https://my.telegram.org)，并使用您拥有的任意手机号码 登录。验证码将发送到 Telegram 应用中，而非通过短信。
2. 选择 **API 开发工具**。
3. 创建应用程序：任意标题和简称（5–32 个字母），平台为**桌面版**。 URL 和描述可留空。
4. 复制 **App api_id**（一个数字）和 **App api_hash**（32 个十六进制字符）。

在登录表单下方的面板中，有“**API ID + 哈希**”字段。您可以在 **API ID** 字段中粘贴一组 `api_id:api_hash`，两个字段将自动填充。一组 即可用于您所有的账户。成功登录后，该信息将以加密形式保存在 该工作区中，且绝不会发回浏览器。

涉及三种不同的凭证：

| 秘密 | 打开 | 托管位置 |
| --- | --- | --- |
| 面板令牌 | TgWitness 网页控制面板 | 数据目录中的 `panel-token.txt`，或 `TGWITNESS_TOKEN` |
| API ID + 哈希值 | 本身不包含任何内容；仅用于标识该应用程序 | 可通过 my.telegram.org 进行内置配对、导入设置或使用您自己的应用程序 |
| 账户授权 | Telegram 账号 | 可通过手机/二维码登录创建，或作为会话导入 |

如果必须通过代理访问 Telegram，请先在 **“账户”→“设置”→“连接设置”→“更改连接路径**”中进行设置。

## 电话号码

1. 打开**“账户**”选项卡，选择**“手机**”标签页，并以国际格式输入号码， 例如 `+44 7700 900123`。空格和连字符将被自动去除。
2. 点击**“继续”**。API ID 和哈希值可留空。
3. 输入 Telegram 发送的验证码（通常发送至 Telegram 应用；短信接收无法保证）。
4. 如果该账户启用了双重验证，请输入该密码。这并非控制面板 令牌，也不是设备密码。
5. 登录后查看显示的账户 ID，然后选择消息来源。

登录凭据和双因素认证（2FA）密码绝不会写入磁盘。

## 二维码

当该账户已在手机或另一台计算机上登录时，请使用此功能。

1. 点击**“QR 码**”→ **显示 QR 码**。API ID 和哈希值可留空。
2. 在已登录的设备上：**设置 → 设备 → 关联桌面设备**，扫描二维码 并确认。
3. 若 Telegram 要求输入双因素认证（2FA）密码，请在 TgWitness 中输入该密码。

该二维码是在本地生成的。二维码会过期；请点击**“生成另一个二维码** ”重新尝试。锁定面板、切换工作区或开始另一轮登录操作将取消 待处理的二维码。

## 认证密钥 + DC ID

授权密钥（Auth Key）是每个 Telegram 会话背后的 256 字节原始授权数据，以 **512 个十六进制字符**的形式表示，并附带数据中心编号 **DC 1–5**。

1. **“Auth key**”选项卡。请粘贴完整的密钥；包含“`…`”的缩短版密钥无法使用。
2. 请选择随密钥提供的 DC ID。
3. 可选输入**用户 ID**。若 Telegram 报告的 账户信息不一致，TgWitness 将拒绝连接。
4. Press **Connect 账号**。

授权密钥（512 个字符）并非 API 哈希（32 个字符）。同一密钥也可 以 JSON 格式导入，详见[“账户 JSON](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#account-json)”。

## 账户文件

打开**“添加账户”→“文件**”，选择最多**四个属于同一账户的文件**（总大小不超过 **8 MiB**），然后点击**“连接账户**”。

- 文件在您的 TgWitness 服务器**内存中**进行转换。上传内容不会被存储， ZIP 文件不会解压到磁盘，也不会连接任何外部服务。
- 生成的会话记录随后将与 Telegram 进行核对。如果文件中包含用户 ID， 则该 ID 必须与 Telegram 报告的账户信息一致。
- 描述不同账户或不同 API 凭据的文件将被拒绝 而非仅选择其中一个。
- **“密码”或“会话文本**”字段包含 TData 本地密码字段，该字段用于粘贴 StringSession 以及**在未登录的情况下读取文件**（无需 联系 Telegram 即可填写表单）。

### Telethon `.session`

|  |  |
| --- | --- |
| 产品简介 | 基于 Telethon 的工具生成的 SQLite 数据库，例如 `my_account.session` |
| 获得以下机构认可： | 表格 `sessions`（连同 `dc_id`、`server_address`、`port`、`auth_key`）和 `version` = 7 或 8 |
| 要求 | 仅有一行授权会话记录；一个封闭且完整的数据库 |

请先关闭创建该文件的程序。如果其旁边存在 `my_account.session-journal` 或 `my_account.session-wal`，则表示数据库尚未最终确定：请正常打开并 关闭原始客户端。删除这些辅助文件可能会导致副本损坏。

### Pyrogram `.session`

|  |  |
| --- | --- |
| 产品简介 | 基于 Pyrogram 的工具生成的 SQLite 数据库 |
| 获得以下机构认可： | 表 `sessions` 包含 `dc_id`、`auth_key`、`test_mode`、`user_id`、`is_bot`；`version` = 2 或 3 |
| 要求 | 生产网络上仅允许一个授权**用户**会话。机器人和测试数据中心（test-DC）会话将被拒绝 |

登录时，系统会将存储的用户 ID 与 Telegram 进行比对。

### 会话 + JSON 对

账户通常以两个同名文件的形式分发，例如 `447700900123.session` 和 `447700900123.json`。请同时选中**这两个文件**。

- 根据 JSON 信息，TgWitness 使用 `app_id`/`api_id` 和 `app_hash`/`api_hash`，因此您 通常无需手动输入 API 凭据。
- 其他字段（如 `phone`、`device`、`sdk`、`app_version`、`lang_pack` 或已保存的 `twoFA` 密码）将被**忽略**。如果该账户启用了双因素认证（2FA），TgWitness 会要求输入验证码。
- 单个 JSON 文件仅为元数据。若无会话文件，请继续通过手机 或 QR 码登录。

### Telegram 桌面版 (TData)

TData 是 Telegram Desktop 应用程序（来自 desktop.telegram.org 的跨平台 应用程序）中的 `tdata` 文件夹。

| 系统 | 默认位置：`tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata`（便携版 Telegram：位于 `Telegram.exe` 旁边） |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

导入方法：

> **并行会话警告。**导入 TData 会复用 Telegram Desktop 的授权 密钥；它不会创建独立的登录账号。请勿在 Desktop 和 TgWitness 中同时使用该密钥。Telegram 可能会因 `AUTH_KEY_DUPLICATED` 导致授权失效，使两个副本均无法使用，直至进行新的登录。
>
>
>
> 请完全退出 Desktop 程序（包括其系统托盘进程），并在 TgWitness 使用导入的会话期间保持该程序关闭。 **请退出程序，切勿注销或撤销会话：** 撤销操作也会使导入的副本失效。如果您需要同时运行两个客户端， 请通过手机或二维码登录 TgWitness 以创建其独立的授权。建议使用 专用账户，但这并不能确保克隆密钥在并行使用时是安全的。
>
>
>
> 这同样适用于导入的 `.session` 文件、StringSession文本及认证密钥十六进制值。 其他拥有独立创建的授权的客户端可以保持登录状态。 请参阅[Telegram的AUTH_KEY_DUPLICATED文档](https://core.telegram.org/api/errors#406-not-acceptable)。

1. 完全退出 Telegram Desktop。
2. 从 `tdata` 中提取仅包含以下两项内容的 ZIP 压缩包：

   - `key_datas`
   - 其旁以 `s` 结尾的 16 个字符的文件，通常为 `D877F783D5D3EF8Cs`

   将整个文件夹及其媒体缓存打包为 ZIP 文件通常会超出限制 （512 条记录，解压后 32 MiB）。 3. 在**“文件**”中选择该 ZIP 文件。如果 Telegram Desktop 设置了**本地密码**，请先在 **“密码”或“会话文本”栏**中输入该密码。这并非双因素认证（2FA）密码。

支持功能：每个存档仅限一个账户，采用现代`key_datas`/`key_data0`/`key_data1`存储技术， 本地密码保护。不支持功能：包含多个已登录账户的文件夹、旧版桌面 布局、受密码保护的ZIP文件，以及独立的原生macOS应用“Telegram for macOS”。

### Telethon StringSession

一行文本，通常以 `1` 开头，长度约为 350 个字符。请将其 作为 `.txt` 或 `.tgwitness-session` 文件（最大 4 KiB）加载，或将其粘贴到 **“通行码”或“会话文本**”下方。仅接受 Telethon 字符串；Pyrogram 和 TDLib 字符串采用不同的格式。

### 账户 JSON

一个 JSON 对象，大小不超过 **64 KiB**，存储在以 **`.json`** 结尾的文件中。

| 字段（别名） | 含义 |
| --- | --- |
| `api_id` (`app_id`) | 应用程序 ID，一个正数 |
| `api_hash` (`app_hash`) | 应用程序哈希值，32个十六进制字符 |
| `string_session` (`session_string`, `session`) | Telethon StringSession 文本，并非文件名 |
| `auth_key` (`auth_key_hex`) + `dc_id` | 完整的 512 个字符的认证密钥和 DC 1–5 |
| `user_id` (`id`) | 可选；在保存授权之前，需与 Telegram 进行比对验证 |

如果同时存在别名和主名称，两者必须一致。示例：

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

第一个示例仅需填写 API 凭据；您可通过手机或二维码登录，或添加会话 文件。不支持批量列表（即账户的 JSON 数组）。

## 识别您拥有的内容

| 您会看到 | 它是一个 | 用法 |
| --- | --- | --- |
| `*.session`；在文本编辑器中打开后，顶部显示为 `SQLite format 3` | Telethon 或 Pyrogram SQLite | **文件**（自动检测） |
| 一个名为 `tdata` 的文件夹，其中包含 `key_datas` | Telegram 桌面版 TData | 将两个文件打包为 ZIP 文件，然后**进入“文件”** |
| 以 `1` 开头的一行文本，约 350 个字符 | Telethon StringSession | **文件** |
| `*.json` 搭配 `app_id`/`app_hash` | 配套元数据 | **文件**及其会话 |
| `*.json` 搭配 `auth_key` 或 `string_session` | 账户 JSON | **文件** |
| 512 个字符 `0-9a-f` | 授权密钥 | **认证密钥** |
| 32 个字符 `0-9a-f` | API 哈希值 | **API ID + 哈希值** |
| 来自 TDLib 应用的 `td.binlog` 或 `db.sqlite` | TDLib 存储 | 不支持 |
| `123456789:AA…` | 机器人令牌 | 不支持 |

## 不受支持的格式

| 格式 | 备选方案 |
| --- | --- |
| TDLib 存储（`td.binlog`）和 TDLib 导出功能 | 通过手机或二维码登录 |
| Pyrogram 会话**字符串** | 请使用 Pyrogram `.session` 文件，或通过手机/二维码扫描 |
| TData 包含多个已登录账户 | 请在 Telegram Desktop 中注销其他账户，或使用各账户各自的会话文件 |
| 机器人令牌 | 不支持：TgWitness 以用户账户身份进行监控 |
| 包含大量账户的 CSV/JSON 列表 | 每个账户添加一个工作区 |
| 测试数据中心（Test-DC）或机器人会话 | 请使用正式版用户账户 |

## 多个账户

点击账户选择器旁边的 **+**，或打开 **“账户” → “设置” → “连接设置” → “工作区**”，输入标签并 登录。

- 支持任意数量的工作区，包括主工作区。每个工作区都有独立的会话、代理 路由、消息源、捕获策略、日志、签名密钥、检查点和导出功能。
- 切换显示的工作区不会暂停其他工作区。
- 日志始终与创建它的账户绑定。使用其他 账户登录需要另一个工作区，且一个账户不能分配给两个 工作区。
- 主面板令牌可控制所有工作区。[授予的访问权限](https://phishdestroy.github.io/TgWitness/zh/docs/reference/access/)可将其他用户的访问范围限制在选定的账户和聊天群组内，并可设置独立的权限和会话限制。
- **账户会**重命名一个工作区，并删除一个已添加的工作区，连同其会话、日志、 来源和签名密钥一并删除。主工作区无法从面板中删除。

## 退出登录

**“账户 → 退出 Telegram**（暂停监控）”会要求 Telegram 结束该 会话，因此该会话也会从账户的“**设置 → 设备**”中消失，并从 工作区保险库中移除。日志、来源、设置和签名密钥将保留，且 日志会记录此次退出操作。 该工作区仍归属于其账户：只有该 账户才能再次连接到它。如果 Telegram 没有响应，该会话仍会在此处被移除， 面板上也会显示相应提示；请在 Telegram 的**“设置”→“设备**”中结束该会话。

## 将 Telethon 会话转换为离线格式

该面板可直接导入 `.session` 文件。若需离线转换为 StringSession 文件，请在项目文件夹中运行：

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

该转换器仅读取 Telethon SQLite 文件（最大 64 MiB），绝不修改输入内容， 不进行任何网络请求，且拒绝覆盖现有的输出文件。

## 确保账户文件的安全

- 请将每个 `.session`、TData ZIP、StringSession、Auth Key 和账户 JSON 视为 密码。TgWitness 会将导入的授权信息保存在其加密保险库中；您可以在 之后删除原始文件。
- 请勿在两个程序中同时运行同一授权。Telegram 可能会撤销该授权 (`AUTH_KEY_DUPLICATED`)，导致两个程序均无法运行。
- 已过期或被撤销的会话无法通过转换恢复。请重新登录。

## 故障排除

| 消息或症状 | 操作指南 |
| --- | --- |
| *无法读取此会话。请关闭其原始客户端……* | SQLite 文件处于打开状态或未完成状态（`-journal`/`-wal` 旁路文件）。请正确关闭原始程序，然后重新复制该文件。 |
| *支持的 Telethon SQLite 模式：7 和 8* / *Pyrogram … 2 和 3* | 该文件由一个非常旧或未知版本的库生成。请改用手机/二维码登录。 |
| *仅支持授权的生产环境用户会话* | 该 Pyrogram 文件属于某个机器人或测试网络。 |
| *TData 存档已超过 512 条记录或 32 MiB* | 仅包含 ZIP 文件 `key_datas` 和 `D877F783D5D3EF8Cs`，不包含整个文件夹。 |
| *无法解密 TData。请检查桌面本地密码* | 在**“密码”或“会话文本**”栏中输入 Telegram 桌面版的本地密码。 |
| *每次仅导入一个 TData 账户* | Telegram Desktop 包含多个账户；请参阅[“不受支持的格式”](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#unsupported-formats)。 |
| *选定的文件描述了不同的账户或 API 凭据* | 仅选择一个账户的文件。 |
| *JSON 中未包含任何受支持的 API 凭据或授权信息* | 请检查 [Account JSON](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#account-json) 中的字段名称。 |
| *仅限 API 元数据* | 该 JSON 文件中未包含会话信息。请添加 `.session` 文件，或使用手机/二维码。 |
| *Auth Key HEX 必须包含全部 512 个十六进制字符* | 密钥被截断或包含`…`。 |
| 账户 ID 与导入的账户不匹配 | 该文件的用户 ID 与 Telegram 报告的不一致；该文件属于另一个账户。 |
| 该账户已属于另一个工作区 | 请打开该工作区，而非重复添加该账户。 |
| 已连接，但**“来源**”中的聊天列表中缺少一个私人群组 | 检查成员资格。筛选器会检查前 1,000 个对话；请在**“参数**”下提高该限制。 |
| 代理连接失败 | 检查路由和 IP 模式。自动 MTProxy 会尝试另一个可用的条目。隐藏 IP 模式将进入等待状态；明确选定的备用模式将在配置的延迟时间过后直接建立连接。参见[路由模式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/#ip-modes)。 |

另请参阅：代理和加密的[连接与安全](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/)设置， 以及登录后数据采集的具体[工作原理](https://phishdestroy.github.io/TgWitness/zh/docs/reference/collection/)。
