# 选择代理

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/proxies/

保持账户连接。明确决定何时其路由可使用服务器的地址。

## 请先选择 IP 模式

01**隐藏 IP**

请使用代理。若所有代理均无法连接，请在断开与 Telegram 的直接连接状态下等待。

02**允许使用备用方案**

在配置的延迟时间过后允许直接连接；当有代理响应时，切换回可用的代理。

03**隧道 / VPN**

允许通过主机的网络建立直连路径。此选项不会安装或验证 VPN。

路由决定连接方式。IP 模式决定是否允许直接连接。

## 让池来维护路由

1. 登录**账户 → 设置 → 连接设置**。
2. 选择 IP 模式和**自动 MTProxy**，或输入固定路由。
3. 保存并运行**“测试 Telegram 连接”功能**。该功能在登录前同样有效。
4. 开始收集后，请确认一条受控消息已成功写入日志。

新的工作区采用具有“隐藏 IP”功能的自动 MTProxy。该代理池整合了四个公共来源，对条目进行探测，保留可用的路径，并替换失效的代理。下载失败时将保留之前的快照。

## 请使用您自己的代理服务器

请输入 SOCKS5 或 HTTP CONNECT 详细信息，粘贴受支持的 Telegram 代理链接，或提供运营商目录。在更改当前活动路由前，请暂停监控。以 `ee` 开头的伪 TLS MTProxy 密钥目前仍不支持。

**轮换、共享和重试设置**

**在“参数”→“自动 MTProxy”下**，可设置失败阈值、冷却时间、计划轮换以及每个代理对应的账户数量。当共享限制设为“1”时，若无可用专属入口，账户将进入等待状态。列表刷新和探测间隔遵循主工作区的设置值。独立代理并不保证拥有独立的出口 IP 地址。

## 将 Telegram 与外部请求区分开来

MTProxy 仅传输 Telegram 流量。时间戳、通知、副本和来源验证则使用独立的 SOCKS5/HTTP 代理、该账户的 SOCKS5/HTTP 路由，或在 IP 模式允许的情况下使用 Direct 协议。这些外部请求可以被禁用。

明确的 `TGWITNESS_PROXY_FEED_PROXY` 配置了数据源下载器的路由。[独立见证](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)器保留其自身的设置。这些控制措施不会安装系统 VPN，也不会重定向浏览器流量。

查看[所有模式、默认设置和来源列表](https://phishdestroy.github.io/TgWitness/zh/docs/reference/connection/#ip-modes)，或[选择谁可以更改账户的路由](https://phishdestroy.github.io/TgWitness/zh/docs/access/)。
