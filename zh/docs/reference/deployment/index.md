# 部署

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/deployment/

可在 Windows、Linux、macOS 或 Docker 环境中将 TgWitness 作为服务运行，通过 HTTPS 访问，并支持备份和更新。

**英语** · [俄语](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [乌克兰语](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [西班牙语](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [葡萄牙语（巴西）](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [土耳其语](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [阿拉伯语](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [乌尔都语](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [印尼语](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [越南语](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [简体中文](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## 选择安装方式

若使用便携包，请从 GitHub Releases 解压 `TgWitness-<version>-windows-amd64-portable.zip`。若采用其他方法，请下载并解压源代码 ZIP 文件或克隆 代码库，然后在项目目录下运行以下命令：

| 安装 | 开始 | 在后台运行吗？ |
| --- | --- | --- |
| Windows 便携版 | `TgWitness.cmd` | 不；请保持窗口打开。 |
| 原生 Windows 版 | `Start.cmd` | 不；请使用可选的登录任务以实现后台运行。 |
| 原生支持 Linux/macOS | `sh start.sh` | 不；请使用 systemd/launchd 进行后台运行。 |
| 在任何受支持的主机上运行 Docker | `docker compose up -d --build --wait` | 是的，只要 Docker 守护进程正在运行。 |
| Windows 版 Docker 辅助工具 | `scripts\Docker.cmd` | 是的；该辅助程序会等待 Web 服务器的运行状态。 |
| Linux/macOS 上的 Docker 辅助工具 | `sh scripts/docker-start.sh` | 是的；该辅助程序会等待 Web 服务器的运行状态。 |

关于第三方应能进行核查的云服务器——该服务器通过 服务商的 API 创建，不使用 SSH，仅可通过 Cloudflare Tunnel 访问——请参阅 [“高可信度部署”](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md)。

原生启动程序会生成一个私有`.venv`，并安装已固定的依赖项。 Docker会在镜像内部构建这些依赖项，无需主机端的Python。首次 设置需要互联网连接。 若未检测到 Python 3.11 及以上版本，`Start.cmd` 会在 为当前 Windows 用户安装 Python 3.12 之前征得用户同意（使用 winget，否则在验证 Python 软件基金会签名后使用 python.org 安装程序）；该过程绝不会请求 管理员权限。Docker 和操作系统服务仍是必备条件。

原生和便携式安装会在其文件夹内使用 `data/live`。Docker 则使用名为 `tgwitness-data` 的卷 位于 `/data`。在您刻意迁移 完整数据目录之前，这些属于独立的安装实例。请勿期望新的 Docker 容器能自动发现原生 账户。

## 安装要求

原生安装需要 Python 3.11 或更高版本，并包含 `venv` 和 `ensurepip`；首次安装依赖项时需要 互联网连接；以及一个可供 `.venv` 写入的项目目录。捆绑的控制面板无需 Node.js 或前端构建。请从 您的常规操作系统账户运行启动器；TgWitness 不需要管理员/root 权限。

- **Windows：**`Start.cmd` 会先检查 `py -3`，然后是 `python`，接着是默认的用户级和 Program Files 安装文件夹，并要求系统版本为 3.11 或更高。如果以上路径均无效，它 将提供上述所述的自动用户级安装选项。`py -3 start.py` 同样有效。 便携版完全不需要 Python。
- **Linux：**`start.sh` 会依次尝试 `python3.13`、`python3.12`、`python3.11`、`python3` 和 `python`，若均不匹配，则会输出适用于 apt、dnf、pacman、zypper、apk 或 Homebrew 的安装命令。 Debian/Ubuntu 系统可能需要安装与所选解释器匹配的 `python3-venv` 软件包。 发行版中较旧的 默认 Python 必须被 Python 3.11 及以上版本替换或补充。
- **macOS：**请安装最新的 Python 3.11+ 发行版；请勿假设操作系统自带的 解释器符合要求。请使用项目目录中的 `python3 start.py`。
- **Docker：**请使用搭载 Compose v2.20 或更高版本的 Docker Engine/Desktop。在 Windows 系统上，Docker Desktop 必须使用 Linux 容器。该容器会自行安装 所需的 Python 依赖项；主机无需单独安装 Python。

请使用持久性本地存储作为数据目录。根据消息、 媒体文件、WAL 增长、导出和备份来规划存储容量；目前尚无基于证据的、适用于所有工作负载的通用最低 磁盘/内存规格。对于没有兼容依赖项轮（wheel）的 CPU 架构和 Python 版本， 可能需要额外的构建工具及其 相应的验证。 “可移植”并不意味着支持所有操作系统或硬件。

已在本机验证 Windows 11/Python 3.12 环境。Linux/macOS/容器配置文件及持续集成（CI） 虽已提供，但尚未在此开发主机上执行。具体范围请参阅 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/) 文件。

## 本地计算机

在 Windows 系统上使用 `Start.cmd`，在 Linux/macOS 系统上使用 `sh start.sh`。`scripts\Setup.cmd` 或 `sh start.sh --setup-only` 可用于 准备运行环境。启动程序在首次使用时会安装依赖项；后续启动 将复用该环境。设置和 Telegram 消息采集需要互联网连接， 但浏览现有记录和生成导出文件可在离线状态下进行。

设置完成后运行 `python start.py --check`，可在不启动收集器的情况下检查本地依赖项、Ed25519、 存储、密钥配置及监听地址。 使用 `--json` 获取结构化输出。传入预期的 `--data-dir`、`--host` 和 `--port`。此检查不会安装软件包、创建日志或连接 Telegram； 它并非完整性或覆盖范围的资格认证。启动时会单独验证 现有日志。`python start.py --help` 同样无需安装。

选项：

运行 start.py 后，请在 Windows 系统上使用 `.venv\Scripts\python.exe`，在 Linux/macOS 系统上使用 `.venv/bin/python` 执行辅助命令，或者先激活该环境。 下文中的 `python -m ...` 示例假设该环境已处于活动状态。

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

环境变量：TGWITNESS_DATA、TGWITNESS_HOST、TGWITNESS_PORT、TGWITNESS_TOKEN。 TGWITNESS_VAULT_KEY_FILE 用于在新安装中选择外部密钥模式；详见下文。 若提供 TGWITNESS_TOKEN，其长度必须至少为 24 个字符；请使用加密 生成的随机值。若未提供，应用程序将在 panel-token.txt 文件中生成一个 256 位的随机令牌。 环境变量覆盖不会重写该文件。请重启以轮换凭据。

数据目录仅允许一个进程拥有。跨平台操作系统文件锁机制可防止 意外的并发写入。请使用一个 Uvicorn 工作进程。控制面板可管理任意数量的 工作区，额外的工作区目录位于 profiles/<id>/ 下。 对于独立的服务实例，请使用独立的目录和端口。SQLite WAL 文件应存储在本地持久化 存储中，而非网络文件系统中。请勿在副本之间共享同一卷。

## Windows 便携版

每个 GitHub 发布版本都包含 `TgWitness-<version>-windows-amd64-portable.zip` 及其 `.sha256`。其中包含来自 python.org 的官方可嵌入式 Python 3.12 运行时 （校验和固定在 `tools/build_portable.py` 中）、TgWitness 及其固定依赖项， 以及三个启动器：

| 文件 | 目的 |
| --- | --- |
| `TgWitness.cmd` | 启动面板；额外选项将被直接传递，例如 `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | 在 `data\demo` 启动合成演示 |
| `TgWitness-Check.cmd` | 在不启动的情况下运行就绪性检查 |

将整个压缩包解压到可写入的文件夹中，例如 `Documents\TgWitness`；请勿 在 ZIP 文件内部或 Program Files 文件夹中运行该程序。运行时使用隔离的模块路径， 因此其他 Python 安装以及 `PYTHONPATH` 均不会对其产生影响。 数据保存在 该软件包的`data`文件夹中。若需更新，请停止 TgWitness，将新版本解压到一个新的 文件夹中，然后将`data`文件夹复制过去。

在 64 位 Windows 系统上使用 Python 3.12 自行构建：

```
python tools/build_portable.py
```

构建程序会验证运行时校验和，将受限依赖项安装到 软件包中，使用嵌入式解释器运行就绪性检查，并将 ZIP 文件和校验和写入 `dist/`。

## 容器

```
docker compose up -d --build --wait
```

这将为 /data 创建一个命名持久卷。 Web 端口映射至 127.0.0.1:8787。 该进程以 UID 10001 身份运行，且已移除 权限，根文件系统为只读，而 /data 和 /tmp 目录可写。 `--wait` 在返回前会检查 Web 服务器的运行状态；它不会建立 Telegram 授权或消息投递。 提供的辅助程序在构建完成后采用 180 秒的就绪超时 设置。初始依赖项的下载可能需要更长时间。

两个基础 Compose 文件均使用项目名称 `tgwitness`，因此将新版本 解压到另一个目录时，系统不会自动选择新的数据卷。请确保该项目仅有一个 部署处于活动状态。对于独立安装，请使用唯一的 `docker compose -p NAME ...` 以及不同的主机端口，并在更新时保留这两个配置。 对于使用不同项目名称的旧部署，请继续使用其原始 名称并添加 `-p`；`docker compose ls` 会列出现有项目。

将 `deploy/env.example` 复制到 `.env`，并将 `TGWITNESS_PORT` 修改为使用不同的回环 端口。例如，`TGWITNESS_PORT=8788` 将控制面板暴露在 `http://127.0.0.1:8788`；容器仍监听 8787 端口。`.env` 被 Git 忽略。

获取初始令牌：

```
docker compose exec tgwitness cat /data/panel-token.txt
```

常用命令：

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` 会在收集器崩溃或 Docker 守护进程 重启后自动重启收集器。在 Linux 服务器上，请使用您所用发行版的 服务管理器（通常为 `sudo systemctl enable --now docker`）启用 Docker 自动启动。在 Windows/macOS 上，请启用 Docker Desktop 的“登录时启动”设置。桌面注销、休眠或 Docker Docker 守护进程都可能中断数据采集。明确停止的容器将保持 停止状态，直到您再次启动它。

在示例配置中，/tmp 分区的上限为 512 MiB。导出构建 改用每个工作区的 `temporary-exports/` 路径，将其映射到持久化 /data 分区。请在此处预留空间 以满足同时导出、日志/WAL 增长、媒体文件及备份的需求。 启动器使用 deploy/constraints.txt 来锁定符合要求的运行时依赖项版本。 Docker 和高保障服务器根据 deploy/requirements.lock 和 deploy/build.lock 文件，通过 pip --require-hashes 进行安装：每个包文件必须与提交中记录的 SHA-256 值相匹配，因此若 PyPI 或镜像站点上的文件被替换，则会被拒绝。 Python 基础 镜像和操作系统软件包仍需通过独立的发布资格认证。

除非您打算销毁日志和密钥，否则请勿使用 `docker compose down -v` 命令。 容器健康状况报告反映的是 Web 服务器的可用性，而非 Telegram 捕获是否成功。 请检查控制面板中的采集器状态、心跳、错误及覆盖事件。

### 独立见证者简介

可选的 `witness` 服务会在其自身的 容器中运行一个[独立的见证节点](https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/)，该节点在 `witness-data` 卷中拥有独立的密钥和日志，而收集器仅拥有一个只读 的见证令牌。在控制面板的**“见证**”页面上创建该令牌，将其 与机器人令牌和频道一起添加到 `.env`，然后启动配置文件：

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

该服务通过 Compose 网络内的收集器访问，地址为 `http://tgwitness:8787` （`TGWITNESS_WITNESS_COLLECTOR` 会覆盖该地址，例如 `/profiles/<workspace ID>` 用于 另一个工作区）。若要使用由他人运行的独立服务器上的见证文件，请在该服务器上使用 `deploy/compose/compose.witness.yaml` ，并将 `TGWITNESS_WITNESS_COLLECTOR` 设置为收集器的 HTTPS 地址；该文件仅包含见证文件。

## 安装已发布的镜像

该网站将在[发布工作流](https://phishdestroy.github.io/TgWitness/zh/docs/reference/deployment/#automated-github-releases) 成功完成且 GHCR 包配置公开后上线。存储库的所有者/名称并未硬编码 到此源代码树中。请使用该发布版工作流摘要中显示的图片。

将 `deploy/env.example` 复制到 `.env`。将 `TGWITNESS_IMAGE` 设置为发布版本，使用 **小写形式的**仓库路径，例如：

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

请单独运行此文件，而非运行 `compose.yaml`：

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

主机上无需源代码构建、Python 或编译器。发布工作流 针对 Linux AMD64 和 ARM64 容器，包括 Docker Desktop 的 Linux 虚拟机。 请使用版本标签或工作流摘要中的 `ghcr.io/owner/repository@sha256:...`。 未配置`latest`标签的动态更新或无人值守的应用程序升级。当 项目名称相同时，镜像和源代码变体将使用相同的数据卷。

## 服务器上的自动 HTTPS 配置

请使用搭载 Docker 的服务器、您自行管理的域名以及持久的本地存储空间。 将域名的 A/AAAA 记录指向该服务器；仅当 IPv6 可访问该服务器时才发布 AAAA 记录。 允许入站 TCP 80 和 443 端口，以及用于证书签发的出站 DNS/HTTPS 流量。 其他服务不得已占用这些端口。

将 `deploy/env.example` 复制到 `.env`，并设置主机名（不包含协议或路径）：

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

使用 HTTPS 覆盖层开始源代码构建：

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

对于已发布的图像，请改用 `deploy/compose/compose.image.yaml` 作为第一个文件。保留 两个 `-f` 参数，以便后续使用状态、日志、更新和停止命令。

Caddy 负责获取和续期证书，将 HTTP 重定向至 HTTPS，并将 请求转发至私有 Compose 网络上的收集器。证书状态 拥有独立的持久化卷。收集器的直接主机端口仅限回环访问。 提供的 Caddy 配置未启用访问日志记录。

打开 `https://watch.your-domain.org` 并输入面板令牌。准备就绪 并不意味着证书已签发或外部可达。如果 HTTPS 尚未 就绪，请检查 DNS、防火墙规则以及：

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

提供的 Caddy 镜像遵循其 `2-alpine` 标签。拉取操作会刷新该镜像； 若需固定基础设施版本，请在部署中固定一个经过测试的摘要。

## 更新与备份

在更新过程中保留 Compose 项目名称和数据量。首先停止 收集器并进行完整备份。对于默认的基于源代码的部署：

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

每次请使用存储库之外的新备份目标，并将其作为 账户访问材料加以保护。示例路径仅供参考；请使用您自己的私有备份 位置。复制整个目录，包括隐藏文件、所有工作区、密钥、 日志和媒体文件。如果已配置外部保险库主密钥，请将其单独备份。 证据 ZIP 文件并非可恢复的应用程序备份。对于 HTTPS，若需保留其证书/账户状态，还应保留 Caddy 卷。

若要进行源代码部署，请获取最新发布文件并运行：

```
docker compose up -d --build --wait
```

若需部署镜像，请将 `TGWITNESS_IMAGE` 替换为所需版本，然后运行：

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

请也使用您安装环境中的 Compose 文件来执行上述停止/复制命令。 请保留 `.env`、自定义配置以及相同的项目名称。`down` 会保留命名 卷；**`down -v` 会将其删除**。请勿在不同操作系统 或 Python 版本之间复制 `.venv`。若需进行原生更新，请先停止 TgWitness，备份其完整数据 目录，替换源文件，并在启动前运行 `python start.py --setup-only`。

更新后，请检查控制面板访问权限、账户身份、监控状态及覆盖范围。 重启不会恢复遗漏的 Telegram 更新。如果未来版本更改了存储格式， 回滚可能需要使用更新前的备份。

## GitHub 自动发布

将该项目推送到已启用 Actions 的 GitHub 仓库后，[发布工作流](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml)即可投入使用。当**发布** GitHub Release（包括预发布版本）时，该工作流会自动运行。仅推送草稿或标签 不会发布软件包。

1. 设置软件包版本和变更日志，然后发布一个标记为 `v` 加上确切的 `pyproject.toml` 版本（例如 `v0.7.0`）的发布版本。
2. 该工作流会验证标签，并运行适用于 Windows/Linux/macOS 的通用 Python、 general/account-import/QR 浏览器、源代码包以及 Docker 检查。此外，还会在 这三种操作系统上使用 Python 3.12 进行全新的原生安装测试。
3. 通过上述检查后，系统会在 QEMU 环境下对 ARM64 镜像进行烟雾测试，将 AMD64/ARM64 镜像发布至 `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`， 并将源代码 ZIP 包、校验和及 Python wheel 文件附加到发布包中。另有一项 Windows 任务负责构建并附加可移植 ZIP 包及其校验和。
4. 首次发布后，请打开 GHCR 包设置，并将可见性 设为“公开”（**Public**），以便匿名拉取图像。仅拥有公开的源代码仓库 并不能保证容器包也会公开。组织政策必须 允许发布包。该工作流使用 `GITHUB_TOKEN`；注册表 密码或 VPS 凭据不应存放在仓库中。

仅通过本地准备工作尚无法确保远程工作流的成功。ARM64 仿真仅为初步验证，并非原生硬件或实时 Telegram 环境的认证。 此功能可自动完成版本打包；启动服务器仍需使用 Compose 命令及其域名/主机先决条件。当新版本发布时，现有服务器不会被 自动升级或重启。

## 远程服务器

请将服务限制在回环接口内并使用 SSH 隧道，或在 反向代理处终止 HTTPS 连接。基础 Compose 文件仅限本地使用；可选的 `deploy/compose/compose.https.yaml` 覆盖层提供 Caddy 以支持配置好的域名。 请勿在 URL 和代理日志中暴露承载令牌。反向代理应限制 请求大小和连接速率。请勿将明文 HTTP 暴露到互联网上。

[deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 目录中提供了 systemd、Windows 登录任务、macOS 用户代理以及 Caddy 的示例。 安装前请审查并调整其路径。 这些仅为模板，并非本地执行的平台配置。常规启动程序不会 注册任何后台服务或任务。

在 Windows 系统上，以无窗口模式启动 `pythonw.exe` 时，启动/服务器诊断信息将存储在 数据目录下的 `logs/server.log` 中（每文件 5 MiB，包含两个轮换备份）。 控制台模式启动时会保留控制台日志。两种模式下 均禁用 HTTP 访问日志记录。请将日志与数据目录一同保护，并在共享前进行审查。

## 重启与数据缺失

系统会保留上次请求的监控状态。如果监控处于活动状态， 启动时将尝试重新连接并恢复所选消息源。手动暂停会清除 该意图。重启失败的情况会被记录并显示在面板中。

StringSession 保留授权状态，但不保留 Telethon 的持久化更新/实体状态。 对话记录会在启动时重新加载。Telegram/Telethon 可在运行过程中恢复部分传输中断， 但 TgWitness 不保证在进程重启后能够实现持久化重放。 每次启动时都会记录前一日志头和离线边界。 监视器每 10 秒检查一次连接状态，并每分钟添加一次心跳信号 （**参数 → 存活记录间隔**）。 短暂的中断可能被忽略；连接的传输通道并不能保证 更新的完整交付。快照是明确的当前历史观察结果，绝非缺失数据的修复。

媒体队列存储在每个工作区的 SQLite 数据库中。一条消息及其对应任务 将以原子方式提交。中断的运行任务将在启动时恢复并重试。 每次下载的基本超时时间为 120 秒，外加按 256 KiB/s 速率计算的文件大小所需时间，且 每种附件类型有 1–2,000 MiB 的限制；超时、速度和重试次数可在**“参数**”中设置。收集器 会跳过大小未知的文件。暂停操作会保留队列中的任务。 重试使用原始的 已观察到的文件描述符，绝不会使用后续编辑消息的最新版本。 临时故障的重试次数有限；媒体 FloodWait 暂停状态在重启后仍会保留。 媒体恢复与 Telegram 更新恢复是分开的，无法重建已消失的文件。

## 备份、恢复与容量

在复制**整个数据目录**（包括 vault.key、 signing.enc、credentials.enc、SQLite 数据库/WAL 文件、媒体文件、令牌、检查点 以及所有配置文件/子目录）之前，请先停止该进程。 在目标服务停止运行时 还原 完整的副本。若保险库密钥缺失或 签名密钥不匹配，将导致启动失败；请勿通过重新生成密钥来强行访问。

请将秘密备份加密并设置访问控制。证据 ZIP 文件便于携带， 用于审查证据文件，而非应用程序备份或 Telegram 会话备份。 本工具不支持自动保留和删除功能。请预留足够的磁盘空间，以存储所有消息、原始 元数据、媒体文件、临时导出文件及备份。

启动验证并导出流记录，而非加载整个日志。 导出操作会锁定已读快照，同时新的 WAL 写入仍可继续；长时间运行的导出 会保留 WAL 页面，因此磁盘容量依然重要。ZIP 文件的上限为 4 GiB （解压后），以匹配独立验证器的默认设置； **通过“参数 → 最大签名 ZIP**” 可提高上限，此类归档文件将使用 `verify.py --max-gib N` 进行验证。其他格式没有事件计数上限。 支持的浏览器会将响应块流式传输到用户选定的文件中。其他浏览器 最多缓冲 128 MiB，并将更大的传输引导至经过身份验证的 CLI：

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

若要使用其他工作区，请从**“导出”→“工作区 ID**”中选用 `--profile ID`； 若要连接远程服务器，请选用 `--format zip|jsonl|csv|html` 或 `--url https://your-server`； 若要更改 5 GiB 的传输限制，请选用 `--max-mib`。仅允许在 回环连接中使用纯文本 HTTP。令牌通过请求头传输，拒绝重定向，现有文件 不会被覆盖，且未完成的下载不会作为已完成文件发布。 如果 TGWITNESS_TOKEN 覆盖了生成的令牌，请使用一个单独受保护的文件 来存储该有效值：panel-token.txt 不会被覆盖操作重写。 该命令的 SHA-256 仅作为传输校验和；请独立验证已签名的 ZIP 文件。

服务器导出文件仍保存在每个工作区的私有`temporary-exports/`中。 成功导出的文件将被清理。中断的导出文件将在 下次工作区启动时被移除，届时该工作区将保持其专属实例锁定状态。该目录属于 存储威胁/容量模型的一部分；请使用加密数据卷。生产级 的数吉字节级数据传输仍需在目标系统上进行兼容性测试。

该面板显示队列中/失败的媒体文件、最旧的待处理媒体文件、可用磁盘空间、Telegram 请求暂停情况，以及访问状态未确认的来源。这些诊断信息并非 完整的端到端交付监控。工作区共享一个进程；一个活动频繁的账户仍可能 影响其他工作区。 独立的工作进程、数据保留/轮换、持久化更新 恢复以及完整的部署认证功能依然存在。控制面板的范围访问权限已在 [“访问与权限](https://phishdestroy.github.io/TgWitness/zh/docs/reference/access/)”部分中记录；独立检查点相关内容详见《 [见证指南](https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/)》。

## 连接与保护选项

连接路径按工作区设置，应在授权前进行配置。 SOCKS5/HTTP CONNECT 使用固定的 python-socks 依赖项。MTProxy 使用 Telethon 的 实验性随机中间传输协议；不支持 Fake TLS ee 密钥。 直接回退取决于所选的 [IP 模式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/#ip-modes)：“隐藏 IP”模式不允许直接回退；显式回退模式在延迟后允许直接回退；隧道/VPN 模式允许直接路由，但不会建立 VPN。这并非全系统范围的网络策略。

对于新安装，TGWITNESS_VAULT_KEY_FILE 应指向一个单独受保护的随机 主密钥文件。请在容器外的 /data 目录下以只读方式挂载该文件。请将每个工作区的 vault.external.json 公开盐元数据与主密钥分别妥善保存。 现有本地保险库需要进行有计划的迁移；设置此变量不会 自动将其转换。消息/媒体存储和导出内容未经过应用程序加密。 请根据需要使用加密卷和足够的私有临时存储空间。

详细操作流程：[连接/安全](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/)设置及 [运行模式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/operations/)。
