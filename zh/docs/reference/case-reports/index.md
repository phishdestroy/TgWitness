# 报告配置与验证

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-reports/

报告过滤器、八种设计模板、内容预设、已保存的变更历史记录以及评估结果均包含在已签名的导出文件中。

将选定的观察结果转化为一份通俗易懂的案件报告：包括案件问题、 范围、已保存的更改、图表、调查结果及来源参考。每份报告都为 接收方提供了核查所交付材料并检查其采集 覆盖范围的途径。

**“信任基础与限制**”部分出现在日志、移交、聊天、 账户和共享报告中。日志和移交 PDF 文件采用与 其已签名的 `report.json` 相同的评估结果。ZIP 清单在已签名的 清单中包含 `case_assessment`。该评估结果随导出材料一同传输。原始 观察结果保留其现有的签名。

## 文档格式与阅读顺序

### 报告工作室

打开**“导出”→“配置”并预览**。依次操作**“数据”→“设计与内容”→“预览”**：

1. 可使用整个工作区，或选择聊天记录、作者、包含 UTC 观察 日期及事件类型的记录。加载目录以搜索聊天记录和作者，或输入 其 Telegram ID。作者过滤器匹配记录的发件人 ID；若删除 通知中未包含发件人，则不会与作者过滤器匹配。
2. 选择页面设计，然后选择图表、参与者标签、对话记录以及 您的书面调查结果。更改设计时，这些选项将保持不变。
3. 生成预览。预览中显示实际计数、活动情况、参与者、样本 记录、已保存的更改以及缺失的消息编号范围。更改选项 会导致预览过时。请在下载 HTML、签名 PDF、 签名 JSON 或证据 ZIP 文件之前保存。

数据预览统计的是完整的稳定日志前缀，而非初始样本。 仅显示的样本行和长列表有边界限制；其省略的计数会 显示出来。后续导出将生成新的稳定快照，因此持续采集可能会 增加这些数字。范围、计数和来源标识包含在 已签名的报告中。打开或预览表单不会将其保存。

**Jurisdiction guidance.** Under Document details, open **Jurisdiction guidance · optional** to choose a jurisdiction and civil/commercial or criminal procedure. The appendix carries the legal basis, source links, preparation notes and research status. Local-language summaries and explanations of collection safeguards are optional. No jurisdiction is selected by default. These choices belong to the workspace, and are excluded from saved layout configurations and implicit sharing-copy defaults. See [defaults, supported reports and research limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/JURISDICTION_GUIDANCE.md).

**选择收件人的副本。** 图表和记录文本均基于所选记录生成。 完整性、保管和覆盖范围描述了完整的源日志。证据 ZIP 文件 包含原始记录及其附件。当收件人仅需接收选定且获准的数据时，请采用[精简移交方式](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#handover-extract) 。

### 读取编辑、删除及缺失的 ID

编辑操作会显示保存前的**“之前**”文本和“**之后**”文本，并突出显示已更改的 词语。删除操作会显示通知出现前保存的最后一个版本。如果未捕获更早的 内容，报告会明确说明。当您仅选择编辑或删除操作时， 先前版本仍作为明确标注的上下文保留在 筛选器之外。 无关的消息不会被添加到这些历史记录中。

**未观测到的消息 ID** 是指在选定聊天记录中的已知编号与 基于日期生成的 ID 范围之间存在的缺口。在将某个 编号判定为未观测之前，需对所有已知源记录进行核查：过滤掉其他作者、事件类型或日期 不会导致虚假缺口。 相邻的已保存消息被标记为上下文。一个缺失的 数字并不能证明该消息曾存在或已被删除；删除通知 和重新检查失败仍属于独立的事件类型。

### 选择一种设计

提供八种页面设计模板，适用于日志和单次聊天记录的 HTML 及签名 PDF 报告。这些模板基于相同的记录和计算结果，仅在封面、 排版、章节标题、表格和行间距方面有所不同。

| 设计 | 行文风格 |
| --- | --- |
| 经典版 | 采用深色封面、各章节编号的传统档案夹。 |
| 编辑说明 | 采用带边框的衬线体标题页，宽边距和窄章节栏。 |
| 简报 | 采用简洁的封面设计，书脊为海军蓝，标题简短，表格排列紧密。 |
| 分析 | 采用调查问卷风格的封面、模块化图表版式及等宽字体图示。 |
| 技术 | 采用带横线的登记表、编号参考栏和精确的对比表。 |
| 概述 | 采用全景式封面设计，留白充裕，并突出显示摘要图表。 |
| 阅读系列 | 采用分栏布局，并将“调查结果”、“范围”、“变更”和“观察日志”等章节分组呈现。 |
| 账本与保证金 | 章节采用编号形式，留有宽边距，图表和表格需完全准确，并单独列出消息记录。 |

设计方案按工作区保存，并记录在已签名的导出清单中。 HTML 支持离线使用，支持浅色和深色主题，并可适应窄屏 及从右到左的语言。原生 PDF 使用捆绑字体；“编辑”设计 包含 Noto Serif 字体，该字体遵循其捆绑的 SIL 开放字体许可证。阅读系列以及 “账本”与“页边距”功能也适用于账户概览、账户聊天和共享副本。

中文、日文和韩文的 PDF 文件还需在服务器上安装合适的字体， 例如 Noto Sans CJK，该字体需在系统范围内部署或放置在 `TGWITNESS_FONT_DIR` 目录中。 若无法使用该字体，ZIP 文件将保留 HTML 和 JSON 格式的报告。

这两种设计均包含无需 JavaScript 即可阅读的日志。对于大型 导出文件，此视图在 8 MiB 的输入配额内最多可显示 500 条完整记录； 报告中会标注该限制，并提供完整查看器及源记录的链接。 账户目录和关系索引描述的是同一阅读样本， 而非所有参与者。完整日志图表保留其单独说明的范围。

### 选择内容

| 目录预设 | 默认包含 |
| --- | --- |
| 案件档案 | 活动、观察时间、参与者、聊天记录及对话记录。 |
| 简报 | 活动概览中不包含参与者排名或对话记录。 |
| 活动回顾 | 活动、观察时间、参与者、聊天记录及其构成，需附来源出处和确切数据。 |
| 自定义报告 | 请自行组合图表、文字记录和预览内容。 |

更改预设时，您的设计、案件详情和书面分析将得以保留。完整性 检查、覆盖范围、限制条件和验证说明在每个设计中均予以保留。 当隐藏图表或笔录时，ZIP 文件中的源记录保持不变。

可选的**“检查笔记**”包含报告作者撰写的提问、方法、发现结果和 结论。在发现结果中需引用源文件和记录编号。 签名将这些作者陈述与 报告一并保存；源观察结果和作者的解读仍可被识别。 简化版交接文件将省略这些私人笔记和完整的病历图表。图表和 检查选项同样适用于病历报告。

可按时间范围筛选活动，查看 UTC 工作日/小时热力图、参与者排名、聊天 排名及记录构成。可选择 5 至 30 个排名组，并使用中立的参与者 别名或账号 ID。未知发件人及其余参与者将显示在单独的 行中。别名仅影响图表显示；源记录中仍保留其真实身份信息。

设计预览基于未保存的草稿进行更新，使用正式版封面、审查和 图表组件，仅限于前 50,000 条源记录中的匹配项。下方的数据预览 计算完整的选定内容。该预览明确 未签名，且不会保留编辑内容。“封面”和“图表”按钮可切换其显示部分。 这并非完整的 PDF 预览。**“保存报告设置**”会将选项应用到 未来的导出中；现有的已签名文件不可更改。PDF 采用所选的封面、 排版、章节布局以及与 HTML 和已签名 JSON 相同的汇总数据。

信任评估、覆盖范围限制和验证说明仍需保留。 隐藏图表或可读转录文本不会从 ZIP 文件中删除权威来源行。 已禁用的图表系列将从分析 JSON 中省略；请使用 “最小化导出”功能来限制来源记录的披露。

数据筛选条件适用于日志报告；账户和共享数据的导出将保留 其自身的采集和披露范围。

共享的设计/图表偏好设置已固定到新的聊天/账户导出文件及账户 共享预览中。账户/共享的语言和隐私设置保持独立； 私人案件和审查笔记不会被复制到这些导出文件中。账户和 共享报告仍以 HTML 格式存在，并由其签名的归档清单提供保护。 日志、 精简版日志移交以及单聊天工具包也提供带签名的PDF文件。

### 图表统计内容

日志活动和热力图统计新消息、历史消息、恢复消息、编辑消息、已删除消息以及 复查时缺失**的消息**，统计依据为采集器记录观察时间（UTC）。心跳 和附件回执不计入统计。 参与者排名仅统计新、历史 及恢复的消息观测：发送者不被视为编辑者或 删除者。重复的观测可能描述同一条 Telegram 消息。

日志分析保留按类型统计的计数、首/末条记录引用以及源文件 `events.jsonl` 的 SHA-256 值。HTML 和 PDF 中的数据均包含精确数值。每日数据桶 在记录超过 366 天后将切换为按月统计；图表将这些数据合并为最多 36 个 等宽区间。 当唯一标识符超过 100,000 个或累计月数达到 1,200 个月时， 相关图表将不可用，但精确的总计数仍可查阅。

快照和账户共享图表仅统计包含的非服务消息行， 并采用其记录的消息时间。共享汇总数据在脱敏 和过滤后计算得出。这些图表最多使用 90 个等宽的 UTC 日期区间，并保留 最多 10,000 个分组值；超出数量将明确声明并进行核对。 最后一个时间间隔可能较短。未知或原始日期不会进入时间图表。

空时间段表示未包含相关记录；如有缺口，请查阅覆盖范围。这些 图表描述了已保存的活动。未知发件人仍作为单独类别，且 每次检查均单独报告。

若包含 `analytics.json` 文件，该文件将受到归档文件签名哈希值的保护。 日志 `report.json` 嵌入了相同的选定聚合值。签名验证 可检测到字节变更。若要核对数据，请使用 `report_analytics.Analytics` 和 `selected` 重新计算日志聚合值，或 使用 `snapshot_analytics.collect` 和 `project` 重新计算快照聚合值。

### Anomaly indicators

**Preview.** Evidence reports add an **Anomaly indicators** section computed by registered processors (`tgwitness/metrics/`, one file per metric). The report names every processor that ran with its version, and prints its method under its table, so the computation can be repeated from `events.jsonl` with `tgwitness.metrics.run`.

| Processor | 功能展示 |
| --- | --- |
| `first_time_posters_over_time` v1 | First-time posters and messages per UTC day. A flag requires at least five first-time posters and three times their median, with message volume at most 1.5 times its median. The baseline uses at least seven observed days within the previous 14 calendar days, after seven days of warm-up. |
| `service_vs_message_ratio` v1 | Distinct saved message numbers per chat and the share used by service messages. It describes a numbering; it does not explain a particular missing number. |
| `join_leave_per_month` v1 | Joins, departures and removals or bans per month, one per person, chat, change and day. |
| `pinned_per_month` v1 | Pin service messages, unpin notices, and pinned messages added or removed between chat-state snapshots, per month. |

**Parameters → Report metrics** selects processors and the number of displayed rows, including in filtered reports. Daily and monthly tables show recent rows, service-share tables rank chats by saved message count. Totals cover every row.

从源代码检出开始，基于同一份虚构期刊构建上述所有八种设计：

```
python tools/build_report_styles.py --output test-results/report-styles
```

打开生成的 `index.html` 文件，以对比完整的 HTML 报告、已签名的 PDF 文件和 ZIP 压缩包。每种设计均基于同一源日志。每次运行时请使用新的输出目录， 以便保留先前已签名的示例。

![虚构的 HTML 档案](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

HTML 页面以案件封面和关键数据开篇。编号证据图谱链接 至每项调查结果、其支持事实、限制条件及独立审查报告。可搜索的 记录和稳定的记录引用在离线查看器中仍可访问。 该设计可适应窄屏设备，并兼容无 JavaScript 支持的主题和浏览器。

已签名的 PDF 文件包含专用的 A4 封面、报告编号和二维码、执行 摘要、证据图、编号调查结果以及文档书签。其页 首和页脚标明了报告信息。二维码用于标识材料；它并非 独立的验证结果。浏览器打印件与该 加密签名的 PDF 文件是分开的。

观察时间轴将记录的观察时段和中断 置于同一条 UTC 时间轴上。空白区域不代表推断出的覆盖范围；详细表格 保留了确切的时间间隔。ZIP 文件包含可读报告、已签名的 JSON、 源记录和验证说明。

生成一份全新的、虚构的英语/俄语/德语档案，其中已安装开发 环境：

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

每个语言目录包含 `report.html`、`report.pdf`、`report.json` 和 `dossier.zip`。现有示例目录绝不会被覆盖。创建过程中不使用任何 Telegram 账户、外部时间戳服务或网络连接。

![虚构的已签名 PDF 文件的前三页](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## 阅读具体案例

对于一个包含 1,200 条记录的日志，其第 1,000 条记录具有经过验证的时间戳， 报告识别出 200 条晚于该时间戳范围的后续记录。 这是 检查点存在的 上限，并非每条消息发送 时间的证明。如果另外三个时间戳文件验证失败或无法验证， 则将其单独计数，且无法得出肯定结论。

一个可用的时间戳必须满足以下所有检查条件：其印记与 检查点匹配，其签名链在加盖时间戳时可追溯至可信的 TSA 根证书，且 检查点的签名、密钥、计数和头部与日志前缀完全一致。 仅解析时间戳或拥有 OTS 收据是不够的。阅读者 必须独立选择可信的 TSA 根证书并重复验证。OTS 需要 其自身的比特币确认检查。

| 报告状态 | 含义 |
| --- | --- |
| 导出时已核对 | 导出工具已执行所述检查；仍需独立重复验证。 |
| 已记录；需审核 | 记录的是基础观察结果或操作员陈述；这并非独立确认。 |
| 本译文未包含以下内容 | 该文本中没有支持这一说法的佐证材料。但也没有说明其他地方不存在此类材料。 |
| 未经独立核查 | 该报告不提供独立的验证结果。 |
| 不完整或不可用 | 某些材料或必需的核查步骤缺失、不完整或未通过。 |

请结合记录的采集覆盖范围，分别审查每一项检查。

## 强配置必须保留的内容

1. 在依赖采集功能之前，请通过 一个独立的可信渠道保留采集器的密钥指纹。将该参考值与导出文件的签名密钥进行比对。
2. 保留带有独立时间戳的检查点，以及（如有使用）位于采集器管理控制范围之外的 见证日志。将其与 导出的日志进行比对，以核查其早期边界。
3. 记录采集范围、缺失部分、过滤条件、限制条件以及采集过程中的变更。 解释与实际申诉相关的缺失时间段，同时明确区分未被观察到的 消息 ID、删除通知和重新核查失败的情况。
4. 保留原始 ZIP 文件及其哈希值。记录每个持有者、传输情况、日期 及目的。同时保留归属的操作员陈述和案件笔记。
5. 对于机密虚拟机，需保留并独立验证引文、挑战、 Intel 证书链、测量数据、确切来源及密钥处理条件。 将证明验证结果与已审查的证据一并保存。

See [verification scope](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope) for the checks of acquisition, archive integrity, time and collection coverage in each mode.

## 收件人审核

请使用可信的 TgWitness 安装版本以及独立获取的指纹：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

证人 ZIP 文件必须来自独立可信的来源；同时保留其密钥 和来源信息。保留命令、工具版本、输出结果、已审核的输入 哈希值以及未解决的问题。信标验证是一项独立的在线检查； 报告渲染器绝不会仅为了显示报告而联系任何服务。

针对特定消息的争议，应引用存档参考信息、权威 文件及记录参考信息，然后描述相关的时间范围、覆盖缺口、 选择标准及佐证材料。对于共享副本，还需审查记录在案的 转换过程及其与源存档的关联。私有过滤器和身份 映射不纳入公开评估范围。

对已签名的 PDF 进行验证可检测受保护字节的更改。请将原始 数字文件和验证结果与任何屏幕截图或打印的阅读副本一并保存。
