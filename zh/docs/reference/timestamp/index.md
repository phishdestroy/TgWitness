# 时间戳

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/timestamp/

签名检查点采用 RFC 3161 时间戳：向认证机构发送的内容以及如何验证响应。

TgWitness 会生成 RFC 3161 请求并验证时间戳授权机构（TSA）的响应。 此手动流程既不选择 TSA，也不提交数据；而证据模式会根据 预定时间表（[证据格式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)）自动完成这两项操作。生成的请求本身 **尚不**构成 **时间戳证明**。

## 证据的约束力

流程图 · 账户观察 → SHA-256 链和 Ed25519 签名; SHA-256 链和 Ed25519 签名 → 签名检查点; 签名检查点 → 精确字节哈希和随机非ce; 精确字节哈希和随机非ce → RFC 3161 请求; RFC 3161 请求 → 独立 TSA; 独立 TSA → 经 TSA 签名的回复; 签名检查点 → 验证数据、非ce值及明确的CA信任关系; 经 TSA 签名的回复 → 验证数据、非ce值及明确的CA信任关系 · 账户观察 · SHA-256 链和 Ed25519签名 · 签名检查点 · 精确字节哈希和随机非ce · RFC 3161 请求 · 独立 TSA · 经 TSA 签名的回复 · 验证数据、非ce值及明确的CA信任关系

**图表转为文本**

1. 账户观察 → SHA-256 链和 Ed25519 签名
2. SHA-256 链和 Ed25519 签名 → 签名检查点
3. 签名检查点 → 精确字节哈希和随机非ce
4. 精确字节哈希和随机非ce → RFC 3161 请求
5. RFC 3161 请求 → 独立 TSA
6. 独立 TSA → 经 TSA 签名的回复
7. 签名检查点 → 验证数据、非ce值及明确的CA信任关系
8. 经 TSA 签名的回复 → 验证数据、非ce值及明确的CA信任关系

采集器的签名将记录与其密钥绑定。一份可信的 TSA 响应可 证明某个检查点在 TSA 声明的时间点确实存在。该 检查点随后可将日志前缀与之绑定。但这并不能确定 每次 Telegram 操作的时间，也无法证明捕获内容的真实性。

## 操作流程

1. 通过独立的可信通道保留采集器的密钥指纹。仅凭 被检查的 ZIP 文件提供的密钥不足以识别采集器。
2. 在**“导出”→“准备时间戳请求**”中，下载所选工作区的 请求 ZIP 文件。解压 `checkpoint.json`、`timestamp.tsq`、`SHA256SUMS` 和 `README.txt`。请勿更改检查点字节。
3. 选择适合该调查的 TSA。使用其 文档中记载的方法提交 `timestamp.tsq`，若为 HTTP 服务则使用 `application/timestamp-query`。 将原始二进制响应保存为 `timestamp.tsr`，并记录端点、检索时间 及请求结果。该请求包含哈希值和随机数而非消息内容； 网络元数据仍会暴露该请求。
4. 请独立于响应内容获取受信任的根证书，以及任何 所需的中间证书。响应中包含的证书并不仅因 被包含其中而自动成为受信任证书。
5. 通过可信的 TgWitness 安装实例，验证：

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

如有需要，请添加 `--intermediates tsa-intermediates.pem` 或 `--openssl /path/to/openssl`。 OpenSSL 必须支持 `ts`。在 Windows 系统上，验证器还会搜索标准的 Git 安装目录。OpenSSL 3.5.9 已使用合成 CA/TSA 进行了本地测试。

1. 在检查点之后导出带签名的日志 ZIP 文件，以便其中包含该前缀。 使用已知的独立指纹进行验证：

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. 将 ZIP 文件、检查点、请求、响应、证书链、验证 结果以及交接记录保存在收集器之外。在接收时重复验证。

从已保存的检查点准备请求：

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

该准备过程会规范化 JSON 格式，并将匹配的检查点包含在归档文件中。 即使输入文件的空格格式不同，也请使用**该归档文件中的检查点字节**进行 TSA 验证。

## 验证范围

| 检查 | 当前行为 |
| --- | --- |
| 数据 | 检查点字节的精确 SHA-256 值必须与响应结果一致 |
| 请求 | 借助`--request`，可对原始查询和随机数进行验证 |
| TSA 签名 | OpenSSL 会验证该签名及其与指定证书颁发机构（CA）的证书链。 |
| 采集器签名 | 由日志验证器使用固定密钥进行独立验证 |
| 撤销 | 不支持自动检索 OCSP/CRL |
| 长期有效性 | 证书过期后不进行归档验证 |
| 计划提交 | 证据模式，默认关闭 |

`--request` 从技术上讲是可选的，但省略它将导致无法验证 原始随机数。对于此完整流程，结果中的 `request_checked` 必须为真。 证书验证遵循已安装 OpenSSL 的规则及验证时间。 长期保存需要单独的证书/撤销证据政策。

有效的加密签名并不自动等同于合格的时间戳，也不构成 法律上的可采纳性认定。如果操作员在 加盖时间戳之前伪造了记录，TSA 仅对这些字节进行锚定；并不能证明其真实性。

## 交接记录

记录案件标识符、发送方和接收方、UTC传输时间及其来源、 目的、文件名/SHA-256值、收集器指纹、序列范围、已知 缺失部分、验证器版本及验证结果。 通过贵组织的流程对该 记录进行签名并独立保存。TgWitness中 未实现多用户保管记录系统。

开发过程中未联系任何独立的实时 TSA。本地测试会生成一个 合成 CA/TSA，用于检查兼容性，并验证对已修改数据、随机数或 CA 的拒绝情况。
