# Telegram · 浏览存档

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/archive/

查找消息。核查来源。构建案情。

01**引入历史记录**

将已启用来源的过往消息拉取到工作区。

02**追踪消息来源**

搜索，然后打开每条结果背后保存的消息。

03**确保交接清晰明了**

您的分析放在一个文件里，签名证据放在旁边。

捕获的记录、识别出的文本以及分析人员的结论均保持独立。

## 加载历史消息

1. **来源 → 范围内的聊天**：检查已启用的聊天，开始观察。
2. **加载完整历史记录**。它按当前的来源列表执行。
3. 随时可以**暂停历史** / **继续历史记录**。重启后请手动继续。
4. 检查每个来源的结果和下载队列，将签名进度报告与导出一起保存。

这会填充工作区。单个聊天的 HTML/JSON 导出是另一回事。[详情](https://phishdestroy.github.io/TgWitness/zh/docs/reference/history/)。

## 先搜索，再决定是否使用 AI

1. **日志**在本地搜索，可按来源和时间筛选。
2. 搜索短语或域名，打开记录及其各个版本。
3. 使用 AI 时，由管理员在**集成**中设置服务商。然后**查询存档**：选择聊天和时间段，查看**发送到模型的数据**，取消勾选不应发出的内容。
4. 检查引用，将回答保存为报告，添加您的笔记。

搜索不需要 AI。报告保存自己的来源和修订版本，与签名日志分开。[服务商设置](https://phishdestroy.github.io/TgWitness/zh/docs/reference/analysis/)。

## 选择您需要的连接方式

| 任务 | 打开 | 设置 |
| --- | --- | --- |
| 让 AI 客户端读取选定的聊天 | **集成 → MCP** | [安装 MCP、创建限定范围的令牌并连接](https://phishdestroy.github.io/TgWitness/zh/docs/reference/mcp/) |
| 识别保存媒体中的文本 | `media.saved`记录 → **识别附件** | [设置本地 Docker worker](https://phishdestroy.github.io/TgWitness/zh/docs/reference/media-analysis/) |
| 将事件发送至 n8n 或 SIEM | **集成 → 外发 webhook** | [添加接收端、校验 HMAC、去重 ID](https://phishdestroy.github.io/TgWitness/zh/docs/reference/webhooks/) |

**哪个访问令牌该填在哪里？**

面板访问是给人用的。MCP 有自己的只读令牌，webhook 有自己的 HMAC 密钥。它们都不需要 Telegram 会话。

[共享控制面板访问](https://phishdestroy.github.io/TgWitness/zh/docs/access/)权限或[配置 MCP 客户端](https://phishdestroy.github.io/TgWitness/zh/docs/reference/mcp/)。

## 提供数据来源和结论

请将报告放在签名 ZIP 旁边。报告是您对来源的解读，ZIP 才是接收方要验证的内容。

[导出与验证](https://phishdestroy.github.io/TgWitness/zh/docs/exports/) · [完整调查流程](https://phishdestroy.github.io/TgWitness/zh/docs/cases/)
