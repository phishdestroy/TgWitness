# 只读 MCP

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/mcp/

将 MCP 客户端连接到选定的工作区和聊天群组，并授予具有时效性且可撤销的访问权限。

将分析员客户端连接到选定的工作区和聊天。TgWitness **在面板进程的 `/mcp` 处提供 Streamable HTTP 服务**。每个连接都有各自的令牌、过期时间和允许使用的工具。MCP 无法发送 Telegram 消息、更改设置或修改已签名的日志。

[工作流指南](https://phishdestroy.github.io/TgWitness/docs/archive/) · [维基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## 安装与检查

使用运行面板的 Python 环境。从源码检出目录执行：

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

安装后，使用常用的数据目录和启动参数重启面板。就绪检查应包含 `[PASS] mcp: streamable-http available`。**Integrations → MCP** 会显示运行时状态以及使用该服务器实际 Python 可执行文件的安装命令。**Re-check** 可在不重新加载页面的情况下刷新此状态；它不会安装软件包或重启服务器。

该 MCP 扩展程序使用官方的[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)。`deploy/constraints-mcp.txt` 锁定了经过测试的 SDK 及其依赖项。

## 签发连接

1. 输入标签并选择客户端可读取的工作区和聊天。
2. 逐个选择工具或使用预设。仅提供已实现的工具。
3. 选择 1、7、30 或 90 天，或在 1 分钟至 90 天之间自定义过期时间。
4. 点击 **Create connection**。令牌会在客户端配置旁显示一次。
5. 复制令牌和配置，然后运行 **Check connection**。它会初始化 MCP 并列出允许使用的工具；**不会读取任何消息**。结果将显示协议版本、工具名称、数量和耗时。
6. 保存凭据后点击 **Done**。轮询会保留表单和单次显示的卡片。锁定面板会清除已显示的机密信息。

列表会显示最近使用情况、上次使用的工具、地址以及过去一分钟内的请求数。**Revoke** 会终止访问权限。**Rotate token** 会吊销旧凭据，并签发具有相同范围、工具和过期时间的替代令牌；请单次复制该替代令牌。面板登录令牌和 Telegram 凭据不能用作 MCP 令牌。

## 连接您的客户端

在面板中选择客户端并复制生成的配置。配置使用机密引用或显式占位符；令牌需单独复制。

| 客户端 | 配置 | 连接 |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP，`type: "http"`，Bearer 请求头 |
| Claude Desktop | `claude_desktop_config.json` | 本地 stdio 桥接 |
| Cursor | `.cursor/mcp.json` | 带环境变量请求头的 HTTP |
| VS Code Local | `.vscode/mcp.json` | 带密码 `promptString` 输入的 HTTP |
| Windsurf | `mcp_config.json` | 带 Bearer 请求头占位符的 HTTP |
| 其他客户端 | URL 和 Authorization 请求头 | Streamable HTTP |

TgWitness 使用 Bearer 令牌，不支持 OAuth 发现。对于远程连接器需要 OAuth 的客户端，请使用本地 stdio 桥接。对于 VS Code，输入变量适用于 **Local** 环境，不会转发到 Copilot 会话。配置参考：[Claude Code](https://code.claude.com/docs/en/mcp)、[Cursor](https://prod.cursor.com/docs/mcp)、[VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)。

本地桥接的标准入口点为：

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

使用客户端本地已安装 MCP 扩展的 Python。在其受保护的环境中设置 `TGWITNESS_MCP_TOKEN`。切勿将凭据放入命令参数和 URL 中。`tgwitness-mcp` 是相同的入口点。旧的 `tgwitness.mcp_bridge` 模块和 `TGWITNESS_ARCHIVE_TOKEN` 名称仍作为兼容路径保留，但会发出警告；新配置请使用 `mcp_server` 和 `TGWITNESS_MCP_TOKEN`。

## Cloudflare Tunnel

转发面板的 `/mcp` 路由并保留 Bearer 请求头。以管理员身份打开 MCP 设置会为本次运行注册面板的当前源（Origin）。若要获得重启后立即可用的稳定地址，请在启动面板前使用面板的 HTTPS 源配置 `TGWITNESS_PUBLIC_URL`。任意 Host 和转发请求头不会注册受信任的地址。Host 和 Origin 检查会拒绝无关的浏览器源。响应使用 `Cache-Control: no-store`；授权值绝不会被记录到日志中。

`*.trycloudflare.com` 地址是临时的。当隧道重启更改主机名时，请更新已配置的公共 URL 以及每个客户端的 MCP URL。对于已保存的客户端配置，请使用稳定的主机名。

## 工具与边界

| 工具 | 读取内容 |
| --- | --- |
| `list_workspaces` | 已授权的工作区 |
| `list_chats` | 已授权的聊天 |
| `search_messages` | 选定时间段内已保存的消息文本 |
| `get_message_versions` | 已捕获的版本和删除观测记录 |
| `get_message_context` | 附近已捕获的消息 ID |
| `get_journal_event` | 单条经过脱敏处理的记录及其来源引用 |
| `get_capture_status` | 采集状态和允许的覆盖范围记录 |

`tools/list` 仅返回授予该连接的工具。对其他工具的调用将被拒绝。此版本不提供群组上下文、事件片段（episode）、术语和回复链工具；未包含它们独立的上下文包后端。

每次读取都会检查令牌、工具以及工作区/聊天范围，包括在数据库操作完成之后。限制为每分钟 60 次请求、每页 50 条记录、每个结果 64 KiB 以及 8 秒的归档截止时间。超时的 MCP 调用会返回工具错误，要求缩小时间段或降低限制。

消息结果包含 `untrusted_content: true`、工作区/聊天/消息 ID、事件序列、已保存的哈希值以及面板链接。原始 Telegram 对象、访问哈希、会话和密钥均被省略。文本截断会予以标记。编辑、删除通知和 `missing_on_recheck` 是不同的观测记录。缺失记录并不能证明某个事件从未发生。

请将已捕获消息中的指令视为证据，切勿将其作为客户端指令。只读访问权限可防止归档被更改；但客户端仍可保留允许其读取的内容。哈希值用于标识已保存的记录并支持完整性检查；它们不能证明 Telegram 作者身份或捕获的完整性。
