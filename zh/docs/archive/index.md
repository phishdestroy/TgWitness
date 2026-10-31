# 浏览存档

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/archive/

查找消息。核查来源。构建案情。

这些工具可在当前主分支中获取。0.7.0 便携版预览版早于这些工具；若要使用该工作流，请检出源代码。

01**引入历史记录**

将已启用的消息源中的历史消息加载到工作区中。

02**追踪消息来源**

搜索存档，并打开每个搜索结果对应的已保存消息。

03**确保交接清晰明了**

请将您的分析结果另行保存，并导出其旁边的签名证据。

捕获的记录、识别出的文本以及分析人员的结论均保持独立。

## 加载历史消息

1. 打开**来源**，检查已启用的聊天，然后开始观察。
2. 选择**“加载完整历史记录**”。运行时将使用当时选定的来源列表。
3. 根据需要使用**“暂停历史**记录”和**“继续历史记录**”功能。重启后，请明确恢复操作。
4. 查看各消息源的处理结果及附件队列。随证据导出文件一同保存经签名的进度报告。

此操作会将可用消息填满工作区。按聊天记录导出 HTML/JSON 文件是一项独立的操作。[历史记录和恢复详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/history/)。

## 先搜索，再决定是否使用 AI

1. 打开**“查询存档”功能**。选择工作区、聊天群组及观察期间。
2. 搜索短语、域名或消息 ID。打开匹配的记录及其保存的版本。
3. 进行 AI 分析时，管理员需先配置服务提供商。在批准请求前，请审查**发送至模型的数据**，并取消勾选不需要的片段。
4. 请核对返回的引用。将答案保存为报告，并添加您自己的修订或注释。

搜索在本地运行，不涉及人工智能。分析报告保留来源引用和修订历史；这些报告与签名日志是分开的。[服务提供商设置和报告](https://phishdestroy.github.io/TgWitness/zh/docs/reference/analysis/)。

## 选择您需要的连接方式

| 任务 | 打开 | 设置 |
| --- | --- | --- |
| 阅读来自 AI 客户端的精选聊天记录 | **集成 → MCP** | [安装 MCP 扩展组件，申请范围限定令牌，并连接客户端](https://phishdestroy.github.io/TgWitness/zh/docs/reference/mcp/) |
| 识别保存媒体中的文本 | `media.saved`记录 → **识别附件** | [配置本地 Docker 工作节点及所需的语言/模型文件](https://phishdestroy.github.io/TgWitness/zh/docs/reference/media-analysis/) |
| 将事件发送至 n8n 或 SIEM | **集成 → 外发 webhook** | [添加接收方、验证 HMAC 并去除事件 ID 的重复项](https://phishdestroy.github.io/TgWitness/zh/docs/reference/webhooks/) |

**哪个访问令牌该填在哪里？**

控制面板访问权限仅限案件审查人员使用。MCP 连接将获得独立的只读存档令牌。Webhook 接收器使用其自身的 HMAC 密钥。所有操作均无需 Telegram 会话文件。

[共享控制面板访问](https://phishdestroy.github.io/TgWitness/zh/docs/access/)权限或[配置 MCP 客户端](https://phishdestroy.github.io/TgWitness/zh/docs/reference/mcp/)。

## 提供数据来源和结论

请将经审核的分析报告与带签名的证据 ZIP 文件一同保存。该报告阐述了您对来源信息的解读；ZIP 文件则允许接收方通过独立可信的指纹和检查点，对保存的记录进行核对。

[导出与验证](https://phishdestroy.github.io/TgWitness/zh/docs/exports/) · [完整调查流程](https://phishdestroy.github.io/TgWitness/zh/docs/cases/)
