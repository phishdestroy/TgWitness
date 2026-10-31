# 只读 MCP

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/mcp/

将 MCP 客户端连接到选定的工作区和聊天群组，并授予具有时效性且可撤销的访问权限。

**当前主要版本：**请使用源代码检出；0.7.0 便携版预览版尚未包含此功能。

[工作流指南](https://phishdestroy.github.io/TgWitness/docs/archive/) · [维基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

从 TgWitness 项目目录安装可选服务器：

```
python -m pip install '.[mcp]'
```

在控制面板中，打开**“集成”→“MCP”**。为连接命名，选择其 工作区和聊天群组，并设定有效期。请一次性复制存档令牌；该令牌 之后无法再次获取。若令牌丢失，请撤销并重新生成。控制面板令牌和 Telegram 凭据并非 MCP 凭据。

## 连接客户端

该面板根据 其[文档中记载的配置](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)，为 **VS Code Local 框架**生成 `.vscode/mcp.json`。 将下载的文件保存至该位置，运行 **MCP：List Servers**，并启动 TgWitness。VS Code 会通过密码输入框提示输入令牌。下载的 JSON 文件中包含提示引用，而非令牌本身。请使用安装了 MCP 扩展的环境中的 Python 可执行文件。

对于其他 stdio 客户端，请运行：

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

请在客户端的受保护环境中设置 `TGWITNESS_ARCHIVE_TOKEN`。请勿将其 放入命令行参数或 URL 中。该桥接器通过控制面板的授权 存档 API 读取数据；它无法直接访问数据库。标准输出仅传输 MCP 消息。

对于远程客户端，请在控制面板旁运行该服务：

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

通过 HTTPS 反向代理将 `/mcp` 转发至 `127.0.0.1:8766/mcp`，同时保留 `Authorization: Bearer …` 头部。禁用授权头 以及请求/响应正文的日志记录。仅在需要时才绑定到本地回环地址之外，使用 `--host` 和 `--public-url`。该端点使用官方 [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 中的 Streamable HTTP。 它支持显式配置的承载凭据，不支持 OAuth 发现； 仅需 OAuth 的客户端不受支持。

**检查协议并进行**初始化将启动一个真正的 MCP 客户端并列出可用工具。此操作 不会获取消息。进行远程检查时，所选的 MCP 服务器将接收 存档令牌。请仅将该权限范围配置给您运营或信任的服务器。

## 范围与成果

可用工具：`list_workspaces`、`list_chats`、`search_messages`、 `get_message_versions`、`get_message_context`、`get_journal_event` 和 `get_capture_status`。不提供 Telegram 操作、配置更改或 批量导出工具。 每次读取都会重新验证工作区/聊天访问权限；过期和被撤销的 凭证将停止生效。限制包括：每分钟每份凭证 60 次 API 请求， 每页 50 条记录，64 KiB 的响应大小，以及 8 秒的 API 超时限制。

消息结果包括工作区、聊天/消息 ID、事件序列、保存的哈希值， 以及一个面板链接。打开链接的查看者必须拥有自己的授权面板 会话。Telegram 原始对象、访问哈希值、文件引用、会话材料 和密钥均被省略。搜索仅针对消息文本，不包括原始字段。 文本内容 受限，截断处会做标记。编辑操作、Telegram删除通知以及 `missing_on_recheck`仍作为独立观察项处理。仅限聊天范围的访问权限无法查看 整个工作空间的操作事件；捕获状态会明确标注此限制。

存档文本属于不可信输入。消息中的指令不赋予任何额外 权限，且不得视为客户端指令。外部 AI 模型可能会 接收其 MCP 客户端请求的任何内容。只读访问权限可防止 对存档进行修改；但无法阻止客户端保留其读取的数据。

哈希值用于标识保存的记录并支持完整性校验。它们并不能 独立证明 Telegram 消息的作者身份，也无法证明每条消息均已被捕获。
