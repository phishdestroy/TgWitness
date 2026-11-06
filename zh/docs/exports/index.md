# 导出与验证

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/exports/

交给对方可以自行对照您的工作区核查的文件。

保留引用导出带签名的 ZIP 文件收件人验证

不熟悉签名和检查点？[修改一条示例记录](https://phishdestroy.github.io/TgWitness/zh/docs/concepts/#chain)，看看哪项检查能发现它。

想将副本存放在收集者之外的地方？请前往 [S3 设置](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3)、[对象锁定](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3-retention)或[经过验证的恢复功能](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3-restore)。

## 保留一份值得信赖的参考资料

请把工作区密钥指纹记在采集器以外的地方。采集期间，也请把签名检查点保存在别处，或运行[独立见证人](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)。接收方正是用这些来核对密钥和日志的早期状态。

## 下载带签名的 ZIP 文件

**导出** → 签名证据 ZIP。其中包含完整日志和签名文件清单。可在 [Report studio](https://phishdestroy.github.io/TgWitness/zh/docs/reports/) 中制作易读的报告，或仅将选定数据作为[移交摘要](https://phishdestroy.github.io/TgWitness/zh/docs/handover/)发送。

HTML、PDF 和 JSON 报告带有各自的封印。CSV 只是工作副本；如需完整性，请使用已验证 ZIP 中的 CSV。

## 请使用可信的 TgWitness 副本进行验证

在项目环境中，使用您自己的指纹和路径：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

通过时会显示 `key_pinned: true` 和 `checkpoint_checked: true`。请将该输出与存档放在一起。检查点必须位于导出末尾或之前。

## 使用验证结果

- **文件：**清单绑定它们的哈希，签名绑定日志。任何改动都会暴露。
- **身份：**您保存的指纹证明这就是您预期的密钥。
- **早期状态：**检查点将导出与移交前保存的日志前缀进行比较。
- **覆盖范围：**空缺、获取结果以及“发送 → 编辑 → 删除”测试表明这套配置实际捕获了什么。

详情：[验证能证明什么、不能证明什么](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope)。

## 设置 S3 异地备份

在工作区中打开**导出 → 异地副本**。支持 AWS S3 以及任何兼容 S3 的存储。它会复制日志分段、已保存文件、带时间戳的检查点和已完成的聊天导出，每一项在离开采集器之前都用 `AES-256-GCM` 加密。

在线演示中这些控件可见，但上传已关闭。请只在您自己的安装中输入真实凭据。

[![完整的异地备份配置面板：端点、区域、存储桶、访问密钥、计划任务、对象锁定及恢复密钥控制](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

展开后显示包含高级选项的完整面板。未显示任何存储凭据。

| 字段 | 输入内容 |
| --- | --- |
| Endpoint | 存储 URL，不含存储桶路径或凭据。示例：`https://s3.example.invalid`。 |
| 地区 | 按服务商要求填写。默认 `us-east-1`。 |
| Bucket | 一个您有写入权限的现有存储桶。示例：`example-case-backup`。 |
| 存储桶中的文件夹 | 前缀，默认 `tgwitness`。其上还会追加每个工作区的前缀。 |
| 访问密钥 ID / 秘密访问密钥 | 两者一起填写，保存在保险库中。之后两者都留空即可保留原值。 |
| 路径风格的地址 | 开启：`endpoint/bucket`。关闭：`bucket.endpoint`。取决于服务商。 |
| 复制间隔 | 1 至 1,440 分钟，默认 5。仅在应用运行时生效。 |
| Object Lock 数据保留 | 天数和模式，前提是存储桶支持 Object Lock。填 0 则保留存储桶默认值。 |

1. 创建存储桶，在不勾选**保留异地副本**的情况下填写目标和凭据，点击**保存异地副本**。
2. **测试连接**会上传一个加密的测试对象。
3. **下载加密密钥**，并保存在远离采集器的地方。没有密钥就无法恢复。
4. 勾选**保留异地副本**，保存，然后**立即复制**，或让计划任务运行。

## 查看数据保留及复制进度

在**更多选项**中选择保留天数以及 `GOVERNANCE` 或 `COMPLIANCE`。TgWitness 会从已上传的对象中读回保留设置并告诉您：已确认、缺失或检查失败。

面板显示上一轮、对象数量、字节数、已复制的日志边界和错误。缺失的本地文件会被报告并在下一轮重试，其余内容继续复制。

上传可走直连、SOCKS5 或 HTTP。如果路由只有 MTProxy，副本会带着错误等待。

## 请将恢复密钥单独保存

密钥 JSON 包含解密密钥、目标、前缀和密钥指纹。恢复时需要它以及具有读取权限的存储凭据。

更改了端点、存储桶或前缀？请重新下载密钥。新的副本会从新目标开始；旧的聊天导出留在原处。

## 在另一台机器上恢复并验证

您需要一个可信的 TgWitness 安装、密钥 JSON、只读存储凭据和一个空文件夹：

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

所有内容会先在私有临时文件夹中检查：完整日志、检查点、文件哈希和大小。不安全的路径、相互冲突的分段，或比其检查点更短的日志都会导致失败，此时不会写出任何内容。

成功后您会得到 `events.jsonl`、`media/`、`checkpoints/` 和 `exports/`。请将命令的 JSON 输出与它们放在一起，并与您自己保存的检查点或见证记录进行比较。
