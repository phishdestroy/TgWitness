# Telegram · 连接账户

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/accounts/

一个工作区 = 一个账户、它的日志和它的密钥。

## 选择登录方式

**账户** → 添加工作区 → 连接设置。请为此使用单独的账户。

- **二维码：**在 Telegram 的“设备”页面扫描并确认。
- **电话号码：**号码、验证码，如有两步验证再输入密码。
- **会话导入：**您自己的会话文件或 Telegram Desktop 数据。

使用内置 API 配置或您自己的 API ID 和 hash。它只用于标识应用，不会让您登录，也不会隐藏任何东西。

**需要先设置代理吗？**

您可以在登录前[选择并测试连接路径](https://phishdestroy.github.io/TgWitness/zh/docs/proxies/)。每个账户都有其专属的连接路径。

## 选择监控内容

1. 选择您需要的聊天、群组或频道。
2. 检查采集设置，包括媒体。
3. 启动后检查连接和最近活动。

账户必须有访问权限。管理员和成员看到的内容不同，日志显示的是这个账户收到的内容。

整个账户？**来源 → 观察范围 → 调查模式**，检查后点击**保存范围**。完整步骤：[调查整个账户](https://phishdestroy.github.io/TgWitness/zh/docs/cases/)。

## 检查完整路径

在测试群组中，用另一个账户发送一条消息，编辑它，再删除它。这三个事件都应出现在日志中。然后[导出并验证](https://phishdestroy.github.io/TgWitness/zh/docs/exports/)。

“已连接”表示连接正常。捕获到测试消息才说明事件确实送达。

## 添加另一个账户

在**账户**中新建工作区，步骤相同。请记下每个账户的密钥指纹，以便日后区分导出。
