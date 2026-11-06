# Telegram · 选择代理

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/proxies/

保持账户在线，并由您自己决定它是否可以暴露服务器的 IP。

## 请先选择 IP 模式

01**隐藏地址**

仅使用代理。如果都不可用，就等待。

02**直接操作作为最后手段**

延迟后直连，一旦有代理可用就切回代理。

03**服务器需位于隧道或 VPN 之后**

可以直连。它不会替您设置或检查 VPN。

路由决定连接方式。IP 模式决定是否允许直接连接。

## 让池来维护路由

1. **账户 → 设置 → 连接设置**。
2. 选择 IP 模式和**自动 MTProxy**，或固定路由。
3. 保存，然后**测试 Telegram 连接**（登录前也可用）。
4. 开始采集，并给自己发送一条测试消息。

新工作区默认使用自动 MTProxy 并开启**隐藏地址**。代理池拉取四个公共列表，检查服务器，保留好用的，替换失效的。

## 请使用您自己的代理服务器

SOCKS5、HTTP CONNECT、Telegram 代理链接或运营方目录。切换前请暂停观察。Fake TLS 密钥（`ee`…）不可用。

**轮换、共享和重试设置**

**参数 → 自动 MTProxy**：失败阈值、冷却时间、轮换、每个代理的账户数。上限为 1 表示账户宁可等待也不共享。不同的代理仍可能共用同一个出口 IP。

## 将 Telegram 与外部请求区分开来

MTProxy 只承载 Telegram 流量。时间戳、通知、副本和代码检查走单独的 SOCKS5/HTTP 代理、账户的 SOCKS5/HTTP 路由，或在模式允许时直连。也可以关闭它们。

`TGWITNESS_PROXY_FEED_PROXY` 设置下载列表所用的路由。[见证人](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)有自己的设置。这些都不会影响您的浏览器或系统网络。

更多：[模式和默认值](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/#ip-modes)，[谁可以更改路由](https://phishdestroy.github.io/TgWitness/zh/docs/access/)。
