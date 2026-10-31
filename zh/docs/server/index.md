# 保持其运行

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/server/

确保采集器在重启后仍可正常运行，且其数据保持完整。

## 选择启动方式

若要进行本地安装，请使用 [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 目录中的[启动器和服务的示例](https://phishdestroy.github.io/TgWitness/zh/docs/start/)。若使用 Docker，请安装 Docker with Compose，并从项目目录运行：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

默认控制面板监听主机的回环地址，端口为 8787。您可以在本地或通过 SSH 隧道打开它。使用第二个命令生成的令牌解锁控制面板。

## 保留整个数据目录

原生安装使用 `data/live`。Docker 则使用持久化卷 `tgwitness-data`。请将日志、账户会话、密钥和运行状态集中保存。签名导出文件虽可作为有效证据，但并非完整的安装备份。

1. 在完成一致性备份之前，请停止数据收集。
2. 将完整的私有数据目录复制到主机外部的受保护存储中。
3. 在依赖备份之前，请先在隔离环境中测试数据恢复。

## 重启后请检查

请确认预期的工作区和密钥、Telegram 连接、已选来源以及新消息捕获设置。保存的 MTProto 状态和补录功能可帮助恢复 Telegram 仍保留的更新内容。但该工具无法重建所有已过期的更新，也无法还原在捕获前被删除的编辑内容。

容器状态正常指 Web 服务器能够响应。请使用受控消息和见证检查来评估数据采集及外部发布情况。

## 仅发布您有意发布的内容

部署参考指南包含 HTTPS 示例、持久卷命令、更新及恢复步骤。提供了用于部署的 Docker 命令；当前的[验证](https://phishdestroy.github.io/TgWitness/zh/docs/reference/verification/)记录列出了实际经过测试的环境。
