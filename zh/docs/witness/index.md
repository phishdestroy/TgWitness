# 设置 Witness 机器人

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/witness/

一个独立进程检查您的日志，并将签名检查点发布到频道。

## 两台主机，两把签名密钥

托管 / 收集器**账户 + 日志**

Telegram 会话收集器的签名密钥

只读检查点端点

← 请求签名回答 →

主机 B / WITNESS**验证 + 保留**

固定收集器指纹 独立见证人签名密钥

自有日志 + 机器人令牌

Witness → Telegram 机器人 API →**您的频道 · 带签名的 TGW1 帖子**

Witness 会自行执行校验。收集器的访问权限仅限只读。机器人发布功能使用 Witness 的连接和令牌；Witness 不会获得任何账户会话权限。

03 / 检查点决策示例答案

最后接受时间**120 条记录**`head 9c7d…`

下一个答案**128 条记录**`head a4f2…`

已通过：计数持续增加，签名已验证，密钥匹配。该见证者保留了这一新边界。

所有解答示例均假设存在有效签名和已固定的密钥。此处的哈希值仅为简略示例。仅凭哈希值数量较多，无法证明整个旧前缀均未发生变化；请将导出数据与保留的检查点进行对比。

## 准备一个机器人和一个频道

用 BotFather 创建机器人，并允许它在您的频道中发帖。请在别处运行见证人：另一台主机，最好由其他人管理，远比在采集器旁边再跑一个进程更有价值。

## “扩展功能”中的三个步骤

1. **只读访问权限。****扩展功能 → 独立见证人**，创建令牌并保存文件。它只读取检查点和健康状态，别无其他。
2. **频道和间隔。**Telegram 频道或 Discord webhook，以及见证人能访问到的采集器地址。保存设置文件。
3. **启动。**将 `witness.json`、`witness-token.txt` 和 `bot-token.txt` 一起放到见证人主机上并运行：

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

等待频道中出现第一条签名帖子，然后将见证人指纹保存在安全的地方。

想用 Discord？将 webhook URL 保存为 `discord-webhook.txt`。一个见证人只发布到一个地方；较长的检查结果在 Discord 上以文件形式送达。

## 选择发布频率

每次检查都发帖可以形成稳定的外部记录：每五分钟一次，相当于每个工作区每天约 288 条帖子。高级设置可以只在有变化或出问题时发帖，使用代理或自定义 Bot API。

**该机器人实际上能证明什么？**

它向采集器请求签名检查点，用预期的密钥核查，并保存自己的签名日志，包括错过和被拒绝的应答。

它检查的是日志状态，本身并不监视 Telegram。为此，请进行受控的送达测试。

## 稍后核查证据

请保留见证人日志、帖子和指纹。[如何核查它们](https://phishdestroy.github.io/TgWitness/zh/docs/reference/witness/#verify)与采集器导出是否一致。
