[TgWitness](../../README.md) / [文档](../README.md) / [文件夹](README.md)

![部署与恢复](../assets/presentation/chapter-operate.svg)

[English](../DEPLOYMENT.md) · [Русский](../ru/DEPLOYMENT.md) · [Українська](../uk/DEPLOYMENT.md) · [Español](../es/DEPLOYMENT.md) · [Português (Brasil)](../pt/DEPLOYMENT.md) · [Türkçe](../tr/DEPLOYMENT.md) · [العربية](../ar/DEPLOYMENT.md) · [فارسی](../fa/DEPLOYMENT.md) · [اردو](../ur/DEPLOYMENT.md) · [हिन्दी](../hi/DEPLOYMENT.md) · [Bahasa Indonesia](../id/DEPLOYMENT.md) · [Tiếng Việt](../vi/DEPLOYMENT.md) · **简体中文**

# 部署与运维

## 选择安装方式

对于便携版软件包，请从
GitHub Releases 中解压 `TgWitness-<version>-windows-amd64-portable.zip`。对于其他方法，请下载并解压源代码 ZIP 文件或克隆
代码库，然后在项目目录下运行以下命令：

| 安装 | 开始 | 在后台运行吗？ |
| --- | --- | --- |
| Windows 便携版软件包 | `TgWitness.cmd` | 不，把窗户开着。 |
| 原生 Windows | `Start.cmd` | 不；请使用可选的登录任务以在后台运行。 |
| 原生 Linux/macOS | `sh start.sh` | 不；请使用 systemd/launchd 进行后台运行。 |
| 在任何受支持的主机上运行 Docker | `docker compose up -d --build --wait` | 是的，只要 Docker 守护进程正在运行。 |
| Windows 上的 Docker 辅助工具 | `scripts\Docker.cmd` | 是的；该辅助程序会监听Web服务器的运行状态。 |
| Linux/macOS 上的 Docker 辅助工具 | `sh scripts/docker-start.sh` | 是的；该辅助程序会监听Web服务器的运行状态。 |

关于第三方应能进行检查的云服务器——该服务器通过
服务商的 API 创建，不支持 SSH，且仅可通过 Cloudflare Tunnel 访问——请参阅
[高保障部署](../HIGH-ASSURANCE.md)。

原生启动程序会创建一个私有`.venv`，并安装已固定的依赖项。
Docker会在镜像内部构建这些依赖项，无需使用主机端的Python。首次
设置需要互联网连接。 若未检测到 Python 3.11 及以上版本，`Start.cmd` 会在
为当前 Windows 用户安装 Python 3.12 之前征得用户同意（使用 winget，否则在验证 Python 软件基金会签名后使用 python.org
安装程序）；该过程绝不会请求
管理员权限。Docker 和操作系统服务仍是必备条件。

原生安装和可移植安装会在其文件夹内使用 `data/live`。Docker 则使用位于 `/data` 的名为 `tgwitness-data` 的卷
。除非您刻意迁移
完整的数据目录，否则这些安装是相互独立的。请不要指望新的 Docker 容器能够自动发现原生
账户。

## 安装要求

原生安装需要 Python 3.11 或更高版本（包含 `venv` 和 `ensurepip`），首次安装依赖项时需要
互联网连接，以及一个可供
`.venv` 写入的项目目录。捆绑的面板无需 Node.js 或前端构建。请从
您的常规操作系统账户运行启动器；TgWitness 不需要管理员/root 权限。

- **Windows：** `Start.cmd` 会先检查 `py -3`，然后是 `python`，接着是默认的用户级和
  “Program Files”安装文件夹，并要求使用 3.11 及更高版本。如果以上方法均无效，它
  将提供上文所述的自动用户级安装选项。`py -3 start.py` 同样有效。
  便携版完全不需要 Python。
- **Linux：** `start.sh` 会依次尝试 `python3.13`、`python3.12`、`python3.11`、`python3` 和
  `python`；若均不符合条件，则会显示适用于 apt、dnf、pacman、zypper、apk 或 Homebrew 的
  安装命令。Debian/Ubuntu 系统可能需要安装与所选解释器匹配的
  `python3-venv` 软件包。 发行版中较旧的
  默认 Python 必须被 Python 3.11+ 版本替换或补充。
- **macOS：** 安装最新的 Python 3.11+ 发行版；不要假设操作系统提供的
  解释器能满足要求。请使用项目目录中的 `python3 start.py`。
- **Docker：** 使用搭载 Compose v2.20 或更高版本的 Docker Engine/Desktop。在 Windows 系统上，Docker Desktop
  必须使用 Linux 容器。该容器会自行安装
  Python 依赖项；主机无需单独安装 Python。

## 本地计算机

在 Windows 上使用 `Start.cmd`，在 Linux/macOS 上使用 `sh start.sh`。`scripts\Setup.cmd` 或
`sh start.sh --setup-only` 用于
准备运行环境。启动器会在首次使用时安装依赖项；后续启动时
将复用该环境。设置和收集 Telegram 数据需要互联网连接，
但浏览现有记录和创建导出文件可在离线状态下进行。

在完成设置后运行`python start.py --check`，以检查本地依赖项、Ed25519、
存储、密钥配置和监听地址，而无需启动收集器。
使用 `--json` 获取结构化输出。传入预期的 `--data-dir`、`--host` 和
`--port`。此检查不会安装软件包、创建日志或连接 Telegram；
它并非完整性或覆盖率验证。启动过程会单独验证
现有日志。`python start.py --help` 同样避免了安装操作。

运行 start.py 后，请在 Windows 系统上使用 `.venv\Scripts\python.exe`，
在 Linux/macOS 系统上使用 `.venv/bin/python` 来执行辅助命令，或者先激活该环境。
下面的 `python -m ...` 示例假设该环境已处于活动状态。

~~~sh
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
~~~

环境变量：TGWITNESS_DATA、TGWITNESS_HOST、TGWITNESS_PORT、TGWITNESS_TOKEN。
TGWITNESS_VAULT_KEY_FILE 用于为新安装选择外部密钥模式；参见 [外部主密钥](../SECURITY-MODEL.md#external-master-key)。
TGWITNESS_TOKEN（若提供）必须包含至少 24 个字符；请使用加密级
随机值。若未提供，应用程序将在 panel-token.txt 中生成一个 256 位的随机令牌。
环境变量覆盖不会重写该文件。请重启以轮换凭据。

一个数据目录只能由一个进程拥有。跨平台操作系统文件锁可防止
意外的并发写入。请使用一个 Uvicorn 工作进程。控制面板可管理任意数量的
工作区，额外的工作区目录位于 profiles/<id>/ 下。
对于独立的服务实例，请使用独立的目录和端口。SQLite WAL 文件应存储在本地持久化
存储中，而非网络文件系统中。请勿在副本之间共享同一个卷。

## Windows 便携包

每个 GitHub 发布版本都包含 `TgWitness-<version>-windows-amd64-portable.zip` 及其
`.sha256`。它包含来自 python.org 的官方可嵌入式 Python 3.12 运行时
（校验和固定在 `tools/build_portable.py` 中）、TgWitness 及其固定的依赖项，
以及三个启动器：

| 文件 | 目的 |
| --- | --- |
| `TgWitness.cmd` | 启动面板；额外选项将被传递过去，例如：`TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | 在`data\demo`中启动合成演示 |
| `TgWitness-Check.cmd` | 在不启动的情况下运行就绪性检查 |

已固定的俄语形态学词典和 PDF 颜色配置文件已打包，供
离线使用。打包规则仅允许在依赖项
`data` 目录中包含其已知的文件路径；若这些目录中出现意外文件，将导致构建失败。

将整个压缩包解压到可写文件夹中，例如`Documents\TgWitness`；请勿
直接在ZIP文件内或Program Files文件夹中运行它。运行时使用隔离的模块路径，
因此其他Python安装以及`PYTHONPATH`不会对其产生影响。 数据保存在
该软件包的`data`文件夹中。若要更新，请停止 TgWitness，将新版本解压到一个新的
文件夹中，然后将`data`文件夹复制过去。

在 64 位 Windows 系统上使用 Python 3.12 自行编译：

~~~sh
python tools/build_portable.py
~~~

## 容器

```sh
docker compose up -d --build --wait
```

这将为 /data 创建一个命名持久卷。
Web 端口映射到 127.0.0.1:8787。该进程以 UID 10001 身份运行，且
已移除权限，根文件系统为只读，而 /data 和 /tmp 目录可写。
`--wait` 在返回前会检查 Web 服务器的健康状态； Telegram 的授权和
消息投递状态会显示在控制面板中。提供的辅助程序在构建完成后采用 180 秒的就绪超时
设置。初始依赖项的下载可能需要更长时间。

两个基础 Compose 文件均使用项目名称 `tgwitness`，因此将新版本
提取到另一个目录时，系统不会自动选择新的数据卷。请确保该项目仅保留一个
活跃的部署。对于独立安装，请使用唯一的
`docker compose -p NAME ...` 以及不同的主机端口，并在更新时保留两者。
对于使用不同项目名称的旧部署，请继续使用其原始
名称并配合 `-p`；`docker compose ls` 列出了现有项目。

将`deploy/env.example`复制到`.env`，并将`TGWITNESS_PORT`修改为使用另一个回环
端口。例如，`TGWITNESS_PORT=8788`将面板暴露在
`http://127.0.0.1:8788`上；容器仍监听8787端口。`.env`被Git忽略。

获取初始令牌：

~~~sh
docker compose exec tgwitness cat /data/panel-token.txt
~~~

常用命令：

```sh
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped`会在收集器崩溃或 Docker 守护进程
重启后重新启动收集器。在 Linux 服务器上，请使用您所用发行版的
服务管理器（通常为 `sudo systemctl enable --now docker`）启用 Docker 自动启动。在 Windows/macOS 上，请启用
Docker Desktop 的“登录时启动”设置。桌面注销、休眠或 Docker 守护进程
Docker 守护进程都可能中断数据收集。明确停止的容器将保持
停止状态，直到您再次启动它。

在示例配置中，/tmp 分区的上限为 512 MiB。导出构建
改用将每个工作区的 `temporary-exports/` 导出到持久化 /data 分区。请在此处预留空间
以满足同时导出、日志/WAL 增长、媒体文件和备份的需求。
启动器使用 deploy/constraints.txt 来锁定符合条件的运行时依赖项版本。
Docker 和高保障服务器根据 deploy/requirements.lock 和
deploy/build.lock 文件，通过 pip --require-hashes 进行安装：每个包文件必须与提交中记录的 SHA-256
值相匹配，因此若 PyPI 或镜像站点上的文件被替换，则会被拒绝。 仅提供源代码的
软件包（如 jieba、pyaes）由启动器、Windows 可移植构建器及 Dockerfile
使用 deploy/build.lock 中锁定的 setuptools（`--no-build-isolation`）进行构建，
因此 pip 不会解析一个单独的、未锁定的构建环境。 Python 基础
镜像和操作系统软件包仍需通过独立的发布资格认证。

除非您打算销毁日志和密钥，否则请勿使用 `docker compose down -v` 命令。
容器健康状况报告反映的是 Web 服务器的可用性，而非 Telegram 捕获是否成功。
请检查控制面板中收集器的状态、心跳、错误和覆盖事件。

### 独立见证人 profile

可选的 `witness` 服务会在自己的容器中运行一个 [独立见证人](../WITNESS.md)，
该见证人在 `witness-data` 卷中拥有自己的密钥和日志，并且仅向收集器提供一个只读
的见证人令牌。 在面板的 **更多工具 → 扩展功能 → 独立见证人** 下创建该令牌，将其
与机器人令牌和频道一起添加到 `.env`，然后启动该配置文件：

```sh
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

该服务会连接到 Compose 网络内的收集器（位于 `http://tgwitness:8787`
，`TGWITNESS_WITNESS_COLLECTOR`
会覆盖该地址，例如 `/profiles/<workspace ID>`
对应
另一个工作区）。如果见证文件位于由他人运行的独立服务器上，请在该服务器上使用
`deploy/compose/compose.witness.yaml`
，并将 `TGWITNESS_WITNESS_COLLECTOR`
设置为收集器的 HTTPS
地址；该文件仅包含见证文件。

## 安装已发布的镜像

将`deploy/env.example`复制到`.env`。将`TGWITNESS_IMAGE`设置为发布版本，并使用
**小写**的仓库路径，例如：

```dotenv
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:1.0.2
TGWITNESS_PORT=8787
```

请单独运行此文件，而不是使用 `compose.yaml`：

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

主机上无需源代码构建、Python 或编译器。该发布工作流
针对 Linux AMD64 和 ARM64 容器，包括 Docker Desktop 的 Linux 虚拟机。
请从工作流摘要中使用版本标签或`ghcr.io/owner/repository@sha256:...`。
未配置移动`latest`标签或无人值守的应用程序升级。当
项目名称相同时，镜像和源代码变体将使用相同的数据卷。

## 服务器上的自动 HTTPS

使用配备 Docker 的服务器、您控制的域名以及持久的本地存储。
将域名的 A/AAAA 记录指向该服务器；仅当 IPv6 可访问该服务器时才发布 AAAA 记录。
允许入站 TCP 80 和 443 端口，以及用于证书签发的出站 DNS/HTTPS 流量。
其他服务不得已占用这些端口。

将`deploy/env.example`复制到`.env`，并设置主机名（不包含协议或路径）：

```dotenv
TGWITNESS_DOMAIN=watch.your-domain.org
```

使用 HTTPS 覆盖层开始源代码构建：

```sh
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

对于已发布的图像，请改用`deploy/compose/compose.image.yaml`作为第一个文件。保留
`-f`这两个参数，以便后续执行status、logs、update和stop命令。

Caddy 会获取并续期证书，将 HTTP 重定向至 HTTPS，并将
请求转发至私有 Compose 网络上的收集器。证书状态拥有
独立的持久卷。收集器的直接主机端口仍仅限回环连接。
提供的 Caddy 配置未启用访问日志记录。

打开`https://watch.your-domain.org`并输入面板令牌。准备就绪
涵盖了容器；证书签发和外部可达性取决于 DNS
和防火墙。如果 HTTPS 尚未就绪，请检查 DNS、防火墙规则以及：

```sh
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

提供的 Caddy 镜像位于其 `2-alpine` 标签之后。执行拉取操作会刷新该镜像；
如果需要固定基础设施版本，请在部署中固定一个经过测试的摘要。

## 更新与备份

在更新过程中保留 Compose 项目名称和数据量。首先停止
收集器，并执行完整备份。对于默认的基于源的部署：

```sh
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

每次请使用位于存储库之外的新备份目标，并将其作为
“账户访问材料”加以保护。示例路径仅供参考；请使用您自己的私有备份
位置。复制整个目录，包括隐藏文件、所有工作区、密钥、
日志和媒体文件。如果已配置外部保管库主密钥，请将其单独备份。
证据 ZIP 文件并非可恢复的应用程序备份。对于 HTTPS，若需保留其证书/账户状态，还应保留
Caddy 卷。

对于源代码部署，请获取新版本的文件并运行：

```sh
docker compose up -d --build --wait
```

若要部署图像，请将`TGWITNESS_IMAGE`更改为所需的版本，然后运行：

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

对于上述停止/复制命令，也请使用您安装环境中的 Compose 文件。
请保留`.env`、自定义配置以及相同的项目名称。`down`会保留命名
卷；**`down -v`会将其删除**。请勿在不同操作系统
或 Python 版本之间复制`.venv`。进行原生更新时，请停止 TgWitness，备份其完整数据
目录，替换源文件，并在启动前运行`python start.py --setup-only`。

更新后，请检查面板访问权限、账户身份、监视状态及覆盖范围。
重启后，TgWitness 将从保存的 Telegram 更新位置继续，并
请求更新过程中遗漏的更新内容。如果未来版本更改了存储格式，
回滚可能需要使用更新前的备份。

## 远程服务器

将服务绑定到回环接口并使用 SSH 隧道，或者在
反向代理处终止 HTTPS 连接。基础 Compose 文件仅限本地使用；可选的
`deploy/compose/compose.https.yaml` 覆盖层为配置好的域名提供 Caddy 服务。
请勿在 URL 和代理日志中暴露承载令牌。反向代理应限制
请求大小和连接速率。请勿将明文 HTTP 暴露到互联网上。

[deploy/](../../deploy/README.md) 中提供了 systemd、Windows 登录任务、macOS 用户代理和 Caddy 的示例。
安装前请检查并调整其路径。
这些仅为模板，并非在本地执行的平台配置。普通启动器不会
注册任何后台服务或任务。

在 Windows 系统上，通过无窗口模式启动 `pythonw.exe` 时，启动/服务器诊断日志将存储在
数据目录下的 `logs/server.log` 中（每个文件 5 MiB，包含两个轮换备份）。
通过控制台启动时，将保留控制台日志。两种
模式下均禁用 HTTP 访问日志记录。请将日志与数据目录一同保护，并在共享前进行审查。

## 重启与缺口

会保留上次请求的观测状态。如果观测处于活动状态，
系统启动时会尝试重新连接并恢复所选数据源。手动暂停会清除
该操作意图。重启失败的情况会被记录并显示在面板中。

TgWitness 会将该账户及每个频道的 Telegram 更新状态
（pts、qts、seq 和日期）存储在工作区保险库中，并在下次启动时恢复这些数据。
随后，客户端会请求在进程停止期间错过的更新，而
定期重新检查会恢复错过的消息，并记录 Telegram 已不再
返回的已保存消息。对话会在启动时重新加载。每次启动都会记录前一次的
日志头、离线边界以及恢复时的更新位置。
监视器每 10 秒检查一次连接状态，并每分钟添加一次心跳
（**更多工具 → 参数 → 每** 记录一次在线状态）。
断开连接和静默期将作为覆盖缺口记录，并附带原因说明。
历史快照作为独立的当前-历史观测结果，与实时记录并列存储。

媒体队列存储在每个工作区的 SQLite 数据库中。一条消息及其任务
会以原子方式提交。中断的运行中任务会在启动时恢复并重试。
每次下载都有 120 秒的基础超时，外加按 256 KiB/s 速率计算的文件大小所需时间，且
每种附件类型有 1–2,000 MiB 的限制；超时、速度和重试次数可在 **更多工具 → 参数** 中设置。 收集器
会跳过大小未知的文件。暂停操作会保留队列中的任务。重试使用原始的
已观察到的文件描述符，绝不会使用后续编辑消息的最新版本。
临时故障的重试次数有限；媒体 FloodWait 暂停状态在重启后仍会保留。
媒体恢复与 Telegram 更新恢复是分开的，无法重建已消失的文件。

## 备份、恢复与容量

`tgwitness backup FOLDER`
在面板持续运行的同时复制数据目录：
先复制检查点，然后通过在线备份 API 复制 SQLite 文件，接着复制键、媒体和
配置文件，因此任何复制的检查点都不比复制的日志更新。`backup-manifest.json`
列出了每个文件的 SHA-256 值和日志头。 要恢复，请停止 TgWitness 并用该文件夹替换
整个数据目录。下次启动时会记录日志是从较旧的副本
恢复的。该记录会将日志与存储在
`TGWITNESS_STATE_DIR`
（位于数据目录外的文件夹）中的日志头进行比较：即 `tgwitness-state`
卷中的
Compose中的&lt;img id="4"/&gt;卷、systemd单元中的`/var/lib/tgwitness-state`
，以及其他情况下的用户本地状态文件夹
。如果没有可写状态文件夹，则无法检测到恢复操作，日志会记录一次相关提示。

如果不执行该命令，请在复制**整个数据目录**（包括 vault.key、
signing.enc、credentials.enc、SQLite 数据库/WAL 文件、media、token、checkpoints
以及所有 profiles/ 子目录）之前停止该进程。 在目标服务停止运行时
还原完整的副本。若保险库密钥缺失或
签名密钥不匹配，将导致启动失败；请勿通过重新生成密钥来强制访问。

请对秘密备份进行加密并实施访问控制。证据 ZIP 文件是便于携带的
审查凭证，而非应用程序备份或 Telegram 会话备份。
系统不会自动删除过期数据。请预留足够的磁盘空间来存储所有消息、原始
元数据、媒体文件、临时导出文件以及备份。

启动验证并导出流记录，而非加载整个日志。
导出操作会锁定一个读取快照，同时新的 WAL 写入仍可继续；长时间运行的导出
会保留 WAL 页面，因此磁盘容量依然重要。 ZIP 文件大小上限为 4 GiB
（解压后），以匹配独立验证器的默认设置；**更多工具 → 参数 → 最大签名 ZIP**
可提高上限，此类存档将通过 `verify.py --max-gib N` 进行验证。其他格式没有事件计数上限。
受支持的浏览器会将响应块流式传输到用户选定的文件中。其他浏览器
最多缓冲 128 MiB，并将更大的传输重定向到经过身份验证的 CLI：

~~~sh
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
~~~

使用来自**导出 → 工作区 ID**的`--profile ID`来切换到另一个工作区，
使用`--format zip|jsonl|csv|html`、`--url https://your-server`连接远程服务器，或
使用`--max-mib`来更改 5 GiB 的传输限制。仅允许在
回环连接中使用纯 HTTP。 令牌通过请求头传输，拒绝重定向，现有文件
不会被覆盖，且未完成的下载不会被发布为已完成文件。
如果 TGWITNESS_TOKEN 覆盖了生成的令牌，请使用一个单独受保护的文件
来存储该有效值：panel-token.txt 不会被覆盖操作重写。
该命令的 SHA-256 仅作为传输校验和；请独立验证已签名的 ZIP 文件。

该面板显示队列中/失败的媒体、最旧的待处理媒体、可用磁盘空间、Telegram
请求暂停情况，以及访问状态未确认的源。这些诊断信息并非
完整的端到端交付监控。工作区共享一个进程；一个存在异常的账户仍可能
影响其他工作区。 独立的工作进程、数据保留/轮换、持久化更新
恢复以及完整的部署认证仍需处理。控制面板的范围访问权限已在
[访问与权限](../ACCESS.md)中记录；独立检查点的内容则在
[见证指南](../WITNESS.md)中说明。

详细步骤：[连接/安全](../CONNECTION-SECURITY.md) 和
[工作模式](../OPERATIONS.md)。
