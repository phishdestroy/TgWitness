# Telegram · 查找问题所在

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/troubleshooting/

从症状入手，一次检查一项。

## 面板要求输入令牌

它要的是启动器所打印文件中的面板令牌。Docker：`docker compose exec tgwitness cat /data/panel-token.txt`。不是 Telegram 验证码，不是机器人令牌，也不是见证人令牌。

## Telegram 无法连接

运行连接检查。如果用的是公共代理，换一个并保存。检查代理类型和密钥格式。刷新列表本身不会切换路由。

## 已连接，但无新消息

1. 观察是否在运行，且在正确的工作区中？
2. 来源是否已选中，且该账户可见？
3. 在测试群组中发送一条独特的消息，然后搜索它。
4. 在日志中查找中断或 Telegram 错误。

安静的聊天只是没有新内容。如果完整性很重要，请进行受控的送达测试。

## 重启后出现 FloodWait 或间隔

FloodWait 是 Telegram 在说“慢一点”。请等它过去并减轻负载，重新连接没有用。重启后 TgWitness 会补上 Telegram 仍保留的内容；其余的是空缺，请记录下来。

## 该机器人已配置完毕，但尚未发布任何内容

见证人是否在运行，机器人能否在频道中发帖，它能否访问采集器和 Bot API？在它的日志中查找发帖失败。采集器端出现轮询并不代表帖子已发出。

## GitHub 令牌集成功能在哪里？

**计划中。**“扩展功能”部分描述了拟议的分叉和构建验证工作流。目前尚无 GitHub 令牌表单，也无法自动验证运行中的安装是否与代码库匹配。请参阅[当前功能状态](https://phishdestroy.github.io/TgWitness/zh/docs/reference/features/)。

报告 bug？请提供版本、操作系统、步骤和去除隐私的错误信息。切勿在公开 issue 中放入会话、令牌、私信或数据目录。
