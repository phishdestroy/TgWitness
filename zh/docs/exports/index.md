# 导出与验证

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/exports/

向接收方提供文件，以便其与采集工作区及其保存的历史记录进行核对。

保留引用导出带签名的 ZIP 文件收件人验证

刚接触签名和检查点？[修改一条示例记录](https://phishdestroy.github.io/TgWitness/zh/docs/concepts/#chain)，看看哪些检查会检测到它。

想将副本存放在收集者之外的地方？请前往 [S3 设置](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3)、[对象锁定](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3-retention)或[经过验证的恢复功能](https://phishdestroy.github.io/TgWitness/zh/docs/exports/#s3-restore)。

## 保留一份值得信赖的参考资料

请将工作区的公钥指纹保存至采集器之外。在采集过程中，请将签名检查点保存在其他位置，或使用[独立见证方](https://phishdestroy.github.io/TgWitness/zh/docs/witness/)。这些参考信息可让接收方验证密钥及早期日志边界。

## 下载带签名的 ZIP 文件

打开**“导出”功能**并创建一个已签名的证据 ZIP 文件。该文件包含完整的工作区日志和已签名的文件清单。使用[“报告工作室](https://phishdestroy.github.io/TgWitness/zh/docs/reports/)”生成易于阅读的报告，或使用[“移交提取](https://phishdestroy.github.io/TgWitness/zh/docs/handover/)”功能仅交付经过筛选和精简的数据。

HTML、PDF 和 JSON 报告均带有各自的签名印章，可单独进行验证。CSV 文件是便于分析的副本；请使用经过验证的 ZIP 文件中的原始 CSV 文件来检查其完整性。若接收方同时需要源记录和附件，请保留带签名的 ZIP 文件。

## 请使用可信的 TgWitness 副本进行验证

在已安装的项目环境中，请替换示例指纹和文件路径：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

当两个引用均通过验证时，结果将报告 `key_pinned: true` 和 `checkpoint_checked: true`。请将验证结果与原始存档一同保存。保留的检查点必须位于导出边界的同一位置或之前。

## 使用验证结果

- **请检查交付的文件：**清单文件绑定了文件的哈希值，而记录签名则绑定了已保存的日志。系统会检测到文件被篡改或记录链断裂的情况。
- **请核对工作区身份：**独立保留的指纹可验证其是否为预期中的签名密钥。
- **对比早期边界：**保留的检查点会将导出内容与移交前保存的日志前缀进行比对。
- **审查采集范围：通过**检查缺失部分、采集结果以及受控的“发送→编辑→删除”测试，描述该配置所捕获的事件。

请将这些结果与收件人的副本一并保留。请查阅[验证结果](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope)以[确定](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope)检查范围，以及对来源主张和采集覆盖范围的单独评估。

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

1. 请先在您的服务提供商处创建存储桶，然后输入其目标位置和凭据。准备过程中请**保持“保留异地副本”**选项未勾选，随后再选择**“保存异地副本”**。
2. 选择**“测试连接”**。此操作将上传一个加密的测试对象，并检查存储端的响应。
3. 选择**“下载加密密钥**”。请将该文件与数据采集器分开存放；恢复数据时需要用到它。
4. 勾选“**保留异地副本**”复选框，然后再次保存。选择**“立即复制**”以手动执行一次，或让计划任务继续运行。

## 查看数据保留及复制进度

在**“更多选项**”中，选择保留天数，并在存储桶支持“对象锁定”（Object Lock）时选择“`GOVERNANCE`”或“`COMPLIANCE`”。TgWitness 会读取已上传对象的保留模式和截止日期。请查看单独的保留结果：已确认、缺少保留或检查失败。

控制面板会报告上一次处理的结果、对象数量、传输字节数、已复制的日志边界以及任何错误。若本地存储介质缺失或发生变更，系统会进行报告，并在下一次处理时重试。该存储介质之后的文件、检查点和队列中的导出任务仍可正常复制。

上传时请使用工作区的 Direct、SOCKS5 或 HTTP 路径。请选择其中一种路径进行 S3 复制；若仅选择 MTProxy 路径，复制操作将因错误而处于待处理状态。

## 请将恢复密钥单独保存

下载的 JSON 文件包含解密密钥、目标设置、工作区对象前缀以及签名密钥指纹。恢复操作既需要此密钥文件，也需要单独的存储凭据（需具备对存储桶的读取权限）。请将它们纳入您的恢复计划中。

如果您更改了端点、存储桶或文件夹前缀，请重新下载密钥文件，以确保其目标路径设置与新路径一致。应用程序会将本地保留的日志、文件和检查点的新副本复制到新目标位置。已从本地上传队列中移除的已完成聊天记录导出文件仍保留在原目标位置。

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

将恢复的材料与您独立保留的检查点或见证记录进行比对，然后审查所需时段内记录的采集覆盖范围。
