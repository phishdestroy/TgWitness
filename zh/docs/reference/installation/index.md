# 安装、验证和更新

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/installation/

只需一条命令即可完成安装、验证签名和哈希值，以及更新和卸载该工具。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文档](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/zh/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[项目](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [快速入门](https://phishdestroy.github.io/TgWitness/zh/docs/reference/quickstart/) · [部署](https://phishdestroy.github.io/TgWitness/zh/docs/reference/deployment/)

**On this page**

- [Install with one command](https://phishdestroy.github.io/TgWitness/zh/docs/reference/installation/#install-with-one-command)
- [Where everything runs](https://phishdestroy.github.io/TgWitness/zh/docs/reference/installation/#where-everything-runs)
- [Full-text search settings](https://phishdestroy.github.io/TgWitness/zh/docs/reference/installation/#full-text-search-settings)
- [Command-line access](https://phishdestroy.github.io/TgWitness/zh/docs/reference/installation/#command-line-access)
- [Verify before running](https://phishdestroy.github.io/TgWitness/zh/docs/reference/installation/#verify-before-running)
- [Update an existing installation](https://phishdestroy.github.io/TgWitness/zh/docs/reference/installation/#update-an-existing-installation)
- [Everyday commands on Ubuntu](https://phishdestroy.github.io/TgWitness/zh/docs/reference/installation/#everyday-commands-on-ubuntu)
- [Remove TgWitness](https://phishdestroy.github.io/TgWitness/zh/docs/reference/installation/#remove-tgwitness)

## 只需一条命令即可安装

引导式安装程序包含一个私有 Python 运行时环境。后续安装请使用同一地址： 每次发布都会将安装程序、哈希值、签名 和构建信息一并更新。

**Linux / macOS (Bash)：**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

在 Ubuntu 服务器上，请以 root 身份运行以安装后台服务。在桌面电脑上， 请以普通用户身份运行。

**Windows（PowerShell 或命令提示符）：**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

在 Windows 系统上无需管理员权限。子 PowerShell 进程会将您的 终端保持打开状态并显示结果。Python 及其依赖项均保留在安装目录中。

在 Ubuntu 上，请选择**“本机”**、**“临时 HTTPS 链接**”或**“自有域名**”。 安装程序会显示控制面板地址和访问密钥。若需临时链接，请在浏览器中打开 该 HTTPS 地址并输入密钥。若需通过远程 服务器进行本地访问，请从您的计算机（`ssh -L 8787:127.0.0.1:8787 user@server`) 并打开 `http://127.0.0.1:8787`。在 macOS 和 Windows 上，本地面板会在您的 浏览器中打开；请保持其终端运行。

在面板中登录 Telegram，并选择要收集的内容。仅安装 并不会自动开始收集 Telegram 数据。

## 一切运行于此

`get.destroy.tools` 是一个**用于提供静态文件下载服务的 Cloudflare Worker**。它不包含 TgWitness 面板、Telegram 会话或用户证据数据库。它不会被路由到 项目 VPS 上。该应用程序在您执行命令的机器上运行。

| 安装 | 程序 | 数据 |
| --- | --- | --- |
| 以 root 身份使用 Ubuntu | `/opt/tgwitness` | 系统服务： `/var/lib/tgwitness-<installation ID>`；请使用 `tgwitness paths` 以获取确切路径。 |
| Linux / macOS 用户 | `~/.local/share/tgwitness` | `data/live` 在该安装环境下。 |
| Windows 用户 | `%LOCALAPPDATA%\TgWitness` | `data\live` 在该安装环境下。 |

设置 `TGWITNESS_INSTALL_DIR` 以选择另一个文件夹。已安装的版本和数据 是分离的。安装程序不会将您的账户、消息或密钥上传至 下载站点。选择 Cloudflare 隧道会将面板流量通过 Cloudflare 传输；使用您自己的域名则会指向您自己的服务器。

每次安装都包含 **START-HERE.html** 和 **START-HERE.txt** 文件，其中包含本地 路径、命令以及代码库的链接。运行 `tgwitness guide` 以打开指南。 在 Windows 上，请使用 `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` 在 PowerShell 中运行。

## 全文搜索设置

[全文搜索](https://phishdestroy.github.io/TgWitness/zh/docs/reference/search/)（预览版）无需任何配置。其索引会在更新后在 后台自动构建。

| 变量或命令 | 效果 |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | 默认：索引保存在 `search/fulltext.sqlite3` 每个工作区的 |
| `TGWITNESS_FULLTEXT=memory` | 无索引文件；每次启动时都会重建索引 |
| `TGWITNESS_FULLTEXT=off` | 不建立索引；仅支持精确文本搜索 |
| `tgwitness index status` | 索引每个工作区的状态 |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | 从签名日志中重建所有索引 |

管理员在**“日志”→“过滤器”→“搜索索引**”中的选择将覆盖 该工作区的变量。命令会查找运行它们的安装 的数据目录；在其他地方，请添加 `--data-dir` 并使用来自 `tgwitness paths`。 如需完整的乌克兰语词典（GPL-3.0 数据），请在 `pymorphy3-dicts-uk` 在 该安装的 Python 环境中。

## 命令行访问

该[命令行](https://phishdestroy.github.io/TgWitness/zh/docs/reference/cli/)（预览版）用于读取存档文件中的脚本和代理程序。

| 变量 | 效果 |
| --- | --- |
| `TGWITNESS_URL` | 面板地址为 `tgwitness search`, `context`, `messages`, `stats` 和 `export`；默认 `http://127.0.0.1:8787` 当设置令牌时 |
| `TGWITNESS_MCP_TOKEN` | 将连接令牌从**“集成”→“MCP**”中存档，该令牌与 MCP 客户端共享； `--token-file` 改为从文件中读取该令牌 |
| `TGWITNESS_DATA` | 当未提供 `--data-dir`、URL 或令牌时，将直接读取数据目录 |

## 运行前请先验证

该单行命令会信任 HTTPS 上的初始脚本。该脚本会在安装前检查 SHA-256 以及应用程序和约束条件上的项目 RSA 签名。 您也可以先下载并验证初始脚本。

公钥为 [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub)。 其 SHA-256 为：

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

请保留来自您信任的代码库版本的此指纹。来自 同一下载服务器的校验和可检测到不匹配；独立受信任的公钥 则是验证发布签名所依据的。

请为下文中的验证下载内容准备一个新的、空的目录。

**Linux / macOS — 在一个新的、空的下载目录中运行**（需要 curl 和 OpenSSL）：

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

如果 `&&` 如果下载、密钥指纹或签名 验证失败，链条将在执行前停止。如果脚本下载与签名验证之间 发生了发布更新，则需重新下载两者。旧版安装程序会保留其不可变的包 URL。

**Windows — 运行前请检查SHA-256：**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

将哈希值与 `install.ps1` 行进行比较。若要进行独立的签名验证， 请使用 OpenSSL（例如在 Git Bash 中）并采用上述相同的公钥指纹：

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Windows 安装程序会通过 .NET 自行验证软件包签名，无需 OpenSSL。这些是独立的 RSA-3072 / SHA-256 签名，而非 Authenticode 签名。 [清单](https://get.destroy.tools/manifest.json)文件记录了软件版本、 精确的 Git 提交、不可变的发布 ID 以及每个构建产物的 SHA-256。该页面提供了 指向相应源代码的链接。清单文件和校验和列表也带有独立的 签名（`manifest.json.sig` 和 `SHA256SUMS.txt.sig`).

## 更新现有安装

**新版本发布后，下载站点会相应更新；当您 再次运行安装程序时，已安装的程序将自动更新。**该工具不提供无人值守更新程序，也不会自动重启 正在运行的集合。当前安装程序通道处于**预览阶段**；它遵循 来自 `main`发布的、经过验证的构建版本，其提交时间可能晚于 GitHub 上最近的编号版本。该页面的版本号来源于 `pyproject.toml`；其提交 和构建 ID 可区分同一预览版本内的更新。

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

请使用与之前相同的安装文件夹和操作系统用户。在停止数据收集后，备份完整的数据 目录； `tgwitness paths` 用于标识该数据。已签名的导出文件 并非完整的安装备份。

**Ubuntu 根目录安装位于 `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

安装成功后：

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

对于 Linux/macOS 用户，请使用其原始 `TGWITNESS_INSTALL_DIR` 或 默认配置，并再次运行第一个安装命令。更新前请关闭前台 面板，更新后重新启动该面板。对于已配置的 Linux 用户 服务，请运行其 `tgwitness restart` 命令。

**Windows：**关闭正在运行的面板，重新运行 Windows 安装命令， 然后在 `bin\tgwitness.cmd` 同一安装环境。安装程序会保留数据、 会话、访问设置和签名密钥。只有当 新环境通过检查后，它才会切换启动器；安装失败时， 原启动器将保留不变。请保留升级前的备份，以应对存储格式的变更。

## Ubuntu 上的常用命令

| 命令 | 结果 |
| --- | --- |
| `tgwitness open` | 当前面板 URL 和访问密钥。 |
| `tgwitness paths` | 精确的程序、数据和指南路径。 |
| `tgwitness guide --print` | 离线操作指南。 |
| `tgwitness status` / `tgwitness logs` | 可用性/服务日志。 |
| `tgwitness stop` / `tgwitness start` | 停止/恢复服务；保留数据。 |
| `tgwitness token rotate` | 替换管理员密钥并结束浏览器会话。 |
| `tgwitness tunnel off` | 禁用公共快速隧道；保留本地面板。 |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | 创建快速隧道链接 / 替换其地址。 |

请参阅[“访问权限](https://phishdestroy.github.io/TgWitness/zh/docs/reference/access/) ”了解同事令牌、会话和 IP 限制，以及 [“安装程序发布](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) ”了解从 GitHub 到 Cloudflare 的发布工作流。

## 删除 TgWitness

本工具不提供卸载程序：只需停止面板并删除其文件夹即可。删除 data 文件夹将永久销毁日志、签名密钥、Telegram 会话以及已保存的文件。 在此之前：

1. 导出所需内容（**导出 → 下载已签名的 ZIP**），并将签名密钥 的指纹和检查点保存在本机之外。若要保留工作区本身，请在停止数据收集后复制 整个数据文件夹。
2. 请从**“您的服务器**”中删除在**“扩展功能 → 24/7 服务器**”下创建的服务器，或通过 `python -m tgwitness.cloud destroy`；服务商将持续向您收取费用，直至这些服务器被删除。
3. 请在 Telegram 的**“设置”→“设备**”中结束每个账户的会话。删除 文件并不会在 Telegram 端注销该会话。

**Ubuntu 根目录安装。**请注意数据文件夹，停止服务，然后删除 该服务、相关文件夹及快捷方式：

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Linux 或 macOS 用户安装。**关闭面板。已配置的 Linux 用户服务 可通过 `systemctl --user disable --now tgwitness-<ID>`；其单位为 `~/.config/systemd/user/`。随后删除 `~/.local/share/tgwitness` （或您的 `TGWITNESS_INSTALL_DIR`) 以及 `~/.local/bin/tgwitness` 快捷方式。

**Windows。**关闭面板并删除 `%LOCALAPPDATA%\TgWitness` （或您的 `TGWITNESS_INSTALL_DIR`）。安装程序不会添加任何服务、计划任务或快捷方式。
