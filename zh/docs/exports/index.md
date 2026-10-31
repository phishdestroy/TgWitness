# 导出与验证

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/exports/

分享一份经过签名的记录，供他人核查。

保留引用导出带签名的 ZIP 文件收件人验证

刚接触签名和检查点？[修改一条示例记录](https://phishdestroy.github.io/TgWitness/zh/docs/concepts/#chain)，看看哪些检查会检测到它。

想将副本存放在收集者之外的地方？请前往 [S3 设置](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3)、[对象锁定](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3-retention)或[经过验证的恢复功能](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3-restore)。

## 保留一份值得信赖的参考资料

请将工作区的公钥指纹保存至采集器之外。在采集过程中，请将签名检查点保存在其他位置，或使用[独立见证方](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)。这些参考信息可让接收方验证密钥及早期日志边界。

## 下载带签名的 ZIP 文件

点击**“导出**”并生成一个带签名的证据 ZIP 文件。该文件包含工作区日志和一份带签名的文件清单。面板过滤器不会限制此完整日志的导出：请在分享前仔细审查相关内容。

独立的 HTML 和 CSV 下载文件便于阅读和分析。请将带签名的 ZIP 文件作为可验证的原始文件保留；单独的 HTML 或 CSV 文件不包含独立的签名。

## 请使用可信的 TgWitness 副本进行验证

在已安装的项目环境中，请替换示例指纹和文件路径：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

当两个引用均通过验证时，结果将报告 `key_pinned: true` 和 `checkpoint_checked: true`。请将验证结果与原始存档一同保存。保留的检查点必须位于导出边界的同一位置或之前。

## 理解结果

- **完整性：**记录的历史数据与导出文件与其签名相符。
- **先前观察：**通过外部检查点，您可以将导出内容与先前保留的日志前缀进行比对。
- **实现方式：**通过受控的“发送 → 编辑 → 删除”测试，将特定事件与捕获的记录进行比对验证。

有效的签名并不能证明每一条 Telegram 事件都已送达、消息来源所言属实，或采集器的时钟时间准确无误。

## 设置 S3 异地备份

在您的运行工作区中，打开**“导出”→“异地副本”**。此可选功能支持 AWS S3 及其他兼容 S3 的服务。它会复制日志片段、已保存的照片和文件、带有时间戳响应的检查点，以及已完成的聊天记录导出。每个对象在上传前都会在收集器上使用 `AES-256-GCM` 进行加密。

在线演示展示了相同的操作界面，但上传功能已被禁用。请仅在您自己运行的工作区中输入存储凭据。

[![完整的异地备份配置面板：端点、区域、存储桶、访问密钥、计划任务、对象锁定及恢复密钥控制](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

展开后显示包含高级选项的完整面板。未显示任何存储凭据。

| 字段 | 输入内容 |
| --- | --- |
| Endpoint | 存储服务的 URL，不包含存储桶路径或凭据。虚构示例：`https://s3.example.invalid`。 |
| 地区 | 您的服务商要求的区域。应用程序默认值为 `us-east-1`。 |
| Bucket | 一个您可以访问的现有存储桶。虚构示例：`example-case-backup`。 |
| 存储桶中的文件夹 | 对象前缀；默认值为 `tgwitness`。应用程序会在此前缀后附加一个由该工作区的签名密钥指纹派生而来的前缀。 |
| 访问密钥 ID / 秘密访问密钥 | 请同时输入两项存储凭据。它们将保存在工作区保险库中。后续保存时，请将两项均留空，以保留已保存的凭据对。 |
| 路径风格的地址 | 根据服务提供商的不同，启用时请使用 `endpoint/bucket`，禁用时请使用 `bucket.endpoint`。 |
| 复制间隔 | 范围为 1 至 1,440 分钟；默认值为 5 分钟。若要执行定时备份，应用程序必须处于运行状态。 |
| Object Lock 数据保留 | 支持 Object Lock 的存储桶的保留天数和模式。若设置为“零天”，则该存储桶将沿用默认保留设置。 |

1. 输入目标位置和凭据。准备过程中请**保持“保留异地副本”**选项未勾选，随后选择**“保存异地副本”**。
2. 选择**“测试连接”**。此操作将上传一个加密的测试对象，并检查存储端的响应。
3. 选择**“下载加密密钥**”。请将该文件与数据采集器分开存放；恢复数据时需要用到它。
4. 勾选“**保留异地副本**”复选框，然后再次保存。选择**“立即复制**”以手动执行一次，或让计划任务继续运行。

**不具备的能力** 该工具不会创建存储桶。当应用程序停止运行时，定时上传也会停止。

## 查看数据保留及复制进度

在**“更多选项**”中，选择保留天数，若您的存储桶支持 Object Lock，请选择 `GOVERNANCE` 或 `COMPLIANCE`。TgWitness 会读取已上传对象的保留模式和截止日期。状态报告将显示“已确认”、“缺少保留”或“验证失败”；仅上传成功并不代表保留已确认。

控制面板会报告上一次处理的结果、对象数量、传输字节数、已复制的日志边界以及任何错误。若本地存储介质缺失或发生变更，系统会进行报告，并在下一次处理时重试。该存储介质之后的文件、检查点和队列中的导出任务仍可正常复制。

上传使用工作区的 Direct、SOCKS5 或 HTTP 路径。通过 MTProxy 无法进行 S3 复制；该应用程序不会回退到直接连接。

**不具备的能力** 仅因上传请求被接受，并不意味着服务提供商必须强制执行 Object Lock。

## 请将恢复密钥单独保存

下载的 JSON 文件包含解密密钥、目标设置、工作区对象前缀和签名密钥指纹。该文件不包含 S3 访问凭据：恢复操作需要单独的凭据，且该凭据需具备对存储桶的读取权限。

如果您更改了端点、存储桶或文件夹前缀，请重新下载密钥文件，以确保其目标路径设置与新路径一致。应用程序会将本地保留的日志、文件和检查点的新副本复制到新目标位置。已从本地上传队列中移除的已完成聊天记录导出文件仍保留在原目标位置。

**不具备的能力** 若无导出的密钥，该工具无法解密副本。存储访问凭据无法替代该密钥。

## 在另一台机器上恢复并验证

请使用可信的 TgWitness 安装版本、下载的密钥 JSON 文件、具有读取权限的存储凭据以及一个空的输出目录。请替换下文中的虚构凭据占位符。

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

在对整个日志、保留的检查点以及保存的媒体哈希值和大小进行核查期间，下载内容和解密后的对象将保存在私有临时存储中。不安全的路径、存在冲突的日志段以及长度短于其检查点的日志均会被拒绝。验证失败时，系统不会发布任何恢复的文件。

恢复成功后，系统将针对副本中可用的内容生成 `events.jsonl`、`media/`、`checkpoints/` 和 `exports/`。请将该命令的 JSON 结果与恢复的内容一并保存。

**不具备的能力** 它不会重建那些从未被记录到日志中的观察结果，也不会取代独立保留的检查点或证人。
