# Telegram · 保持其运行

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/server/

让采集器保持运行，数据在重启后依然安全。

## 选择启动方式

原生：[启动器](https://phishdestroy.github.io/TgWitness/zh/docs/start/)加上 [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 中的服务模板。Docker，在项目文件夹中执行：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

面板监听 localhost:8787。在本地或通过 SSH 隧道打开，使用第二条命令输出的令牌。

## 保留整个数据目录

原生：`data/live`。Docker：`tgwitness-data` 卷。日志、会话和密钥必须放在一起。签名导出是证据，不是备份。

1. 先停止采集。
2. 将整个数据目录复制到主机以外的安全位置。
3. 在信任它之前，先在单独的安装上试着恢复。

## 重启后请检查

检查工作区和密钥、连接、来源，以及新消息是否进来。TgWitness 会补上 Telegram 仍保留的内容，而不是停机期间发生的一切。

容器“健康”表示 Web 服务器有响应。采集是否正常，要看测试消息和见证人。

## 仅发布您有意发布的内容

HTTPS、卷、更新和恢复见部署参考。实际测试过的内容：[验证记录](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/)。
