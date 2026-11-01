# 快速入门

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/quickstart/

安装和启动 TgWitness 的所有方法：Windows 安装包、Python、Docker 以及综合演示，并附带初步测试。

**英语** · [俄语](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [乌克兰语](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [西班牙语](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [葡萄牙语（巴西）](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [土耳其语](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [阿拉伯语](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [乌尔都语](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [印尼语](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [越南语](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [简体中文](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness 是一款用于监控您账户可访问的 Telegram 群组和频道的独立应用程序， 它在本地运行并拥有独立的数据目录。

**初次访问？**在连接账户前，[请先体验演示版](https://phishdestroy.github.io/TgWitness/zh/docs/reference/quickstart/#explore-the-interface)。 [选择代理、Witness、数据导出或服务器设置的相关指南](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)。

## 安装并启动

[通过 GitHub Actions 采集（预览版）](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

请选择一种方式。发布版本发布后，即可获取便携版下载：

| 主机 | 无需安装 | 来源：Python 3.11+ | Docker：Engine/Desktop 搭配 Compose 2.20+ |
| --- | --- | --- | --- |
| Windows | 从 GitHub Releases 中提取 `TgWitness-<version>-windows-amd64-portable.zip`，双击 `TgWitness.cmd` | 双击 `Start.cmd` | 双击 `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

对于源码方式，请[下载并解压当前的 `main` 分支](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip)， 或克隆仓库：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

如果未找到合适的 Python，`Start.cmd` 会提议为您的 Windows 用户安装 Python 3.12（通过 winget 或带签名的 python.org 安装程序）。如果缺少 Python，`start.sh` 会打印 适用于您的 Linux 发行版或 macOS 的确切安装命令。 首次从源码启动会自动创建 `.venv` 并安装依赖项。

Docker 负责构建应用程序并在后台启动它；无需在主机上安装 Python。当 容器运行正常时，`scripts\Docker.cmd` 和 `scripts/docker-start.sh` 会输出控制面板地址和令牌。在所有受支持的主机上，相应的 Docker 命令如下：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

打开 **http://127.0.0.1:8787**。使用 Docker 辅助程序或第二个 Docker 命令生成的令牌，或者在便携式或源代码安装中读取 **data/live/panel-token.txt 文件**。继续执行下方的 **“连接 Telegram**”步骤。 原生安装和 Docker 安装使用独立的存储空间； 启动 Docker 不会导入现有的原生日志。

对于服务器，[部署](https://phishdestroy.github.io/TgWitness/zh/docs/reference/deployment/)涵盖自动 HTTPS、重启、 发布图片、更新和备份。

## 探索界面

1. 在便携包中运行 **TgWitness-Demo.cmd** ，在 Windows 源 文件夹中运行 **scripts\Demo.cmd** ，或在 Linux/macOS 上运行 `sh start.sh --demo` 。首次从源代码启动会先创建 `.venv` 并安装依赖项。
2. 访问 **http://127.0.0.1:8787**。
3. 本地演示会自动打开示例日志。无需复制令牌即可直接进行本地访问。

演示消息均为虚构。演示模式无法连接真实的 Telegram 账户。

## 连接 Telegram

> [!警告] **请勿使用任何您无法承受损失的资源。**我们强烈建议不要连接 个人或重要账户，也不要在您珍视的账户上创建 API ID / 哈希值。 Telegram 会不按规律且往往永久封禁账户，无论使用何种客户端。 测试运行是否顺利取决于 Telegram 自身，而非 TgWitness，且无法保证后续效果。

1. 如果原生演示程序正在运行，请将其停止，并运行 **Start.cmd** 或 `sh start.sh`。 否则，请继续运行上文启动的实时安装程序。
2. 请使用与您的安装方式对应的面板令牌来打开面板。
3. 如果您需要使用代理，请在**“账户”→“设置”→“连接设置”→“更改连接路径**”中进行保存。
4. 在**“账户**”中，输入您的手机号码并点击**“继续**”，选择 **“二维码”→“显示二维码**”，或选择文件并点击**“连接账户**”。 **API ID + 哈希**为可选项：工作区将使用其已保存或导入的配对， 或来自内置池中的有效配对。若要使用您自己的应用程序，请将一组 `API ID:API Hash`配对粘贴到API ID中。 如需完整的授权密钥，请选择**“授权密钥**”，粘贴全部 512 个十六进制 字符，并选择提供的 DC ID。用户 ID 为可选项，若输入则会被勾选。
5. 请完成您选择的登录方式：手机/验证码/双因素认证（2FA），通过 已登录的 Telegram 应用确认二维码，或导入受支持的授权会话。
6. 请核对显示的账户 ID。开放**来源**：您的聊天记录会自动加载；请添加您的群组。
7. 在**“选择要保留的更改**”下，选择事件类别或 **“消息、编辑和删除**”预设，然后保存监控设置。
8. 请分别选择附件设置，然后点击**“开始监控**”。

API 凭据用于识别您的应用程序；它们本身并不能 授权任何账户。私人群组无需公开用户名，但您的账户必须具备访问权限。

对于现有账户，请参阅[账户和会话格式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/)：面板 支持 Telethon StringSession、Telethon/Pyrogram SQLite、单账户 TData ZIP 以及受支持的账户 JSON。同时选择一个会话及其配套的 JSON 文件， 然后按**连接账户**。二维码登录同样 可用，并支持相同的可选 API 设置。不支持 TDLib、机器人会话以及 CSV/JSON 账户清单。

对于多个账户，请使用**账户 → 导入账户**并选择其受支持的 会话文件。配套的 JSON 文件按基本名称（basename）配对；每个导入的账户 都会获得各自的工作区。请参阅[批量导入与账户组](https://phishdestroy.github.io/TgWitness/zh/docs/reference/accounts/#bulk-import-and-account-groups)。

要添加另一个账户，请点击账户选择器旁边的 **+**，或打开 **“账户” → “设置” → “连接设置” → “工作区**”，或使用**“账户”功能**。各个工作区拥有独立的会话、 日志、密钥、来源和队列。切换视图时，其他采集器将继续运行。 在此安装环境中，同一个 Telegram 账户不能分配给两个工作区。 工作区数量没有限制；它们共享一个进程，因此容量取决于机器性能。

实时面板令牌用于保护您对 Telegram 授权及已保存 材料的访问权限；它与 Telegram API 凭据相互独立。只有明确启动的、 直接访问的本地演示版本才会自动获得访问权限。远程/代理演示版本仍使用 `data/demo/panel-token.txt`。

## 查看与导出

- **日志：**可按来源和事件类型搜索和筛选记录。
- 选择一项事件，查看其原始记录、来源信息及保存的版本。
- 编辑详情显示可用的编辑前/编辑后内容。删除详情显示 最后捕获的内容（如有）；未知行为者仍为未知。
- **导出格式：**带签名的 ZIP、JSONL、CSV 以及离线 HTML。
- **完整聊天记录导出**（来源 → 完整聊天记录导出）：将单个聊天窗口的全部可见 历史记录下载为包含 `chat.json`（Telegram-export 风格）和可读 `chat.html` 的签名包。私聊功能仅在该账户为群组成员时可用。此为当前 快照，并非对已删除或先前编辑过的消息的重建。 使用`python verify.py chat-export.zip --fingerprint TRUSTED_SHA256` 验证副本。
- **保存检查点：**将签名日志的边界保持在收集器之外。
- **下载签名运行收据：**保留收集器的程序/版本记录。
- **准备时间戳请求：**向时间戳授权机构发起离线请求； 按照 [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/timestamp/) 中的说明获取并验证响应。
- **验证日志：**检查事件签名和链节。ZIP 导出功能还会检查媒体文件。

支持的浏览器可将大型导出文件直接保存到指定文件中。其他浏览器 最多缓存 128 MiB。在服务器运行期间，流式 CLI 支持 更大规模的下载，而无需缓存整个响应：

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

若要添加另一个工作区，请通过**“导出”→“工作区 ID**”添加 `--profile ID`。 若要添加远程服务器，请添加 `--url https://your-server`。默认传输限制为 5 GiB；`--max-mib` 可更改该限制。带签名的 ZIP 内容默认另有 4 GiB 的未压缩 验证限制（通过**“参数**”可提高该限制；请使用 `verify.py --max-gib N` 验证此类存档）。请使用可信的验证器副本以及 独立保存的密钥指纹/检查点来验证该存档。

## 查看安装指南

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check`用于检测本地依赖项、签名支持、存储、密钥配置以及 监听地址。该工具不会安装任何内容，也不会连接到Telegram。若端口 已被占用，可能意味着已有另一个实例正在运行。请使用另一个`--port`实例，或先停止当前实例。

启动程序将安装到`.venv`目录下。辅助的`python -m tgwitness...`命令必须 在Windows系统上使用`.venv\Scripts\python.exe`，或在Linux/macOS系统上使用`.venv/bin/python`， 除非该环境已激活。

## 会话、保护与操作

封闭且一致的 Telethon SQLite `.session` 文件可通过 `python -m tgwitness.sessions account.session --out account.tgwitness-session` 在本地进行转换，随后 加载到 Account 中。还支持直接文件导入和 QR 码登录。有关登录格式、SOCKS5、 HTTP CONNECT、MTProxy 及外部主密钥的详细信息，请参阅 [CONNECTION-SECURITY.md。](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/)

**暂停观察**将停止数据采集。**锁定**仅关闭浏览器访问权限。 关闭标签页不会终止采集进程。停止该进程才会中断 数据采集；历史快照无法还原所有遗漏的编辑或删除操作。 了解[数据采集在事件策略、附件队列、 账户隔离及重启行为方面的运作原理](https://phishdestroy.github.io/TgWitness/zh/docs/reference/collection/)。

会话和密钥均经过加密。消息内容、媒体文件及导出数据需要存储在 加密磁盘或卷上。签名基于可信密钥来验证数据完整性； 但无法证明消息源自 Telegram，也无法防止由控制收集器及其密钥的操作员 伪造数据。

请阅读 [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/operations/) 了解备份/恢复操作，阅读 [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/deployment/) 了解托管方案，并访问 [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 查看服务示例。已安装的 控制面板还包含一份离线设置指南，地址为 `/guide.html`。

实际验证情况及现有局限性 记录在 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/) 和 [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) 中。
