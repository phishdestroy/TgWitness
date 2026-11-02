# “案件看板”参考

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-board/

书签、精确高亮、操作片段、讨论、范围访问以及“案件看板”所使用的签名注释历史记录。

“案件看板”为调查团队提供了一个共享的已保存材料工作视图。您可以对 观察结果添加书签、突出显示具体段落、保存一系列操作，并与同事进行讨论。 卡片会保留其来源引用和已签名的修订历史。团队注释保留在 工作区中，可与原始 Telegram 观察结果区分开来。

[证据模型](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/) · [访问](https://phishdestroy.github.io/TgWitness/zh/docs/reference/access/) · [报告](https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-reports/)

![综合调查信息流](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

## 处理案件

在“标准”或“专家”模式下打开**“调查”→“案件看板”**。语言设置随面板而定。 在日志记录或已保存的聊天消息旁点击**“**添加**到案板**”，或选中该条目并按 **B** 键。 单击即可将书签添加到“收件箱”。可编辑其标题、标签和备注，或将其移动到 收藏夹。修改后的卡片会附加带签名的修订版本；删除卡片时会保留历史记录。

对于首个案例，请选择一个采集集，并添加能回答某个问题的记录。使用“评论” 功能审查解读结果，然后使用**“演示**”功能逐一浏览卡片及来源上下文。 在[“报告工作室](https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-reports/)”中准备 交付成果时，请单独选择“案件看板”中的材料。保存切片不会自动配置报告的数据过滤器。

在已保存的聊天消息中选中文字，即可显示**“突出显示 → 板”**。选择颜色并 添加注释。服务器会核对精确的引文及已保存版本，包括表情符号、从右到左（RTL）文本和 组合符号。界面不会通过被遮盖或转换的文本映射选定内容。

在同一聊天中按住 Shift 键点击两条记录以**进行“切片**”，使用**“按时间切片**”，或保存 日志中当前的聊天、时间段和事件类型过滤条件。已保存的切片具有其自身的权威性 谓词：在日志中打开它时，也会应用多个聊天、消息数量限制和参与者 过滤条件。 **“显示自书签添加以来的记录**”可筛选出后续添加的记录。更改日志 过滤器将退出该切片。在“人员”中**，“按此人操作切片**”功能使用记录的参与者 ID； 该功能不会假设消息作者曾编辑、删除或对消息做出过反应。

“切片”对话框会在允许创建前预览计数。“`all`”包含所有记录类型， 包括快照、编辑、删除、反应、成员资格/服务更新、自身操作、 按钮、媒体结果、恢复的消息以及未来事件类型。该选项描述了 已保存的观察结果。 “未知聊天”删除通知属于独立上下文， 仅对拥有整个工作区访问权限的用户可见，且绝不会被归因于所选的任何聊天。

收藏集具有声明的聊天范围。空范围表示整个工作区。一个收藏集 不能包含其范围之外的卡片；受聊天范围限制的参与者无法阅读范围更广的 收藏集。收件箱是用于未分配卡片的虚拟收藏集。 搜索和筛选仅涵盖可见 卡片；讨论串和提及继承父卡片的访问权限。已删除的评论在讨论中会显示 “墓碑”标记。不会记录查看历史。

**“演示”模式**会打开所选集合中的所有卡片，提供“卡片”、“来源上下文”和“团队 评论”视图，以及键盘上的“上一张/下一张”控制键。该模式不提供任何编辑控件。普通 信息流采用分页显示；“演示”模式按页加载列表，并每次仅检索一张卡片的详细信息。

## 权限

所有操作均需`view`、工作区/聊天范围及`board.read`权限。`board.write`权限用于添加卡片、 评论、移动操作以及开启/审核状态。`board.manage`权限用于管理采集集、 确认/驳回状态，以及修订/删除他人卡片。状态是团队 的决策，而非加密验证结果。

访问表单预设：审核员 = 只读；分析师 = 读写；操作员 = 读写/管理， 此外还包含其现有权限。现有授权不会自动获取新权限。 主管理员拥有所有权限，并以**“主管理员**”身份发布内容。请使用命名授权 进行归属标注。提及列表仅显示当前能够阅读完整父卡片内容的访问者。

针对聊天 A 的授权无法获取 A+B 的卡片或片段，即使通过猜测其 ID 或提供 虚假的 `target.chat_id` 也不行。目标元数据由服务器根据已签名的事件哈希解析得出。 在响应之前，会过滤收集项、讨论次数、相关卡片和实时通知。 导出操作需要同时具备`export`和`board.read`权限；现有导出者若无板访问权限，将 获得不含团队笔记的普通证据存档。SSE会在每次批量处理前重新核查当前授权。

## 已存储的合同

与观察记录类似，注释也是以事务方式写入工作区中一个仅追加的 SQLite 表中。 `annotations.jsonl` 是从与 `events.jsonl` 相同的读取快照中导出的精确规范格式文件。 不存在第二个相互冲突的注释存储，也没有 `board.activity` 日志事件。

每行内容应精确包含：

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

上文的简短示例展示了封装结构；实际有效载荷包含其模型 默认值和由服务器解析的目标字段。API 请求架构位于 [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json) 目录下，由 `python tools/build_board_schemas.py` 通过运行时 Pydantic 模型生成。额外的请求字段将被拒绝。若未提供 ID，则由 服务器端自动生成。 调用方无法提供 作者、时间、快照和签名信息。命名授权 ID 遵循 Access 现有的 16 位十六进制格式；卡片 ID 为 32 位十六进制。

规范 JSON 采用 UTF-8 编码，对象键按顺序排序，标记之间无空格，Unicode 未转义， 且不包含 NaN 或无穷大值。注释哈希值是包含 `format: "tgwitness-annotations-v1"` 以及所有七个信封字段（直至 `previous_hash`）的规范对象的 SHA-256 哈希值。 此格式标签将其哈希域与观察结果区分开来。 签名采用 Ed25519 算法，基于 32 个原始哈希字节生成。序列从 1 开始。修订版本保留卡片 ID，并在 ``supersedes`` 字段中注明前一个 注释哈希；修订版本不能更改聊天范围。移动、状态和删除操作均为 独立记录。SQLite 表不支持 UPDATE 和 DELETE 操作。

`case-board.json` 包含 `{statement, signature}`。规范陈述由 工作区密钥签名，并包含 `format: "tgwitness-case-board-v1"`、`public_key`、`created_at`、 `journal_head`、`meaning` 以及 `state`。状态为确定性重放：`annotations_head`、一个 有序的 `items` 数组（包括集合、卡片、评论及已删除项）以及 `status_history`。 各项在不同修订版本中均保留其最后一次注释哈希值、序列号、作者和时间，以及原始 创建者和创建时间。重放过程会检查修订版本、 父项、集合引用以及重复的操作 ID。`manifest.json` 和新的检查点 也会绑定 `annotations_head`。独立保留一个检查点，以检测数据截断或使用 复制的签名密钥进行的改写。

### 文本版本

`range.start` 是基于零的 Unicode 码点偏移量，`length` 是正的码点计数， 且 `quote` 必须与目标事件中 `payload.text` 或 `payload.caption` 的精确子字符串完全一致。 不应用 NFC/NFKC、大小写转换或字符规范化。 Python 字符串切片和 JavaScript 的 ``Array.from(text)`` 实现了相同的索引机制。标记与 ZWJ 表情符号的组合可能 占用多个码点。``range.version`` 是目标事件的哈希值，而非当前消息 版本或 Telegram 的 UTF-16 实体偏移量。后续编辑绝不会自动重新定位高亮标记。

### 切片标识与时间

`query` 函数仅接受一个 `chat_id` 或非空的 `chat_ids` 列表，可选的包含起始点 `from` 和结束点 `to`， 包含消息 ID 范围（仅限一个聊天），kinds: "all" 或精确/前缀通配符类型的 `kinds: "all"`， 显式 `actors`，`search`，`hide_system` 以及 `include_unscoped`。日志类型组将展开为 其精确的谓词。 搜索使用日志的 NFC/不区分大小写的有效载荷搜索，且不更改 已签名的源文本。日期需要指定时区，并规范化为 UTC。 日期用于过滤 **observed_at**。Telegram 的 `source_at` 将单独显示。若删除操作没有 源时间戳，则不会生成虚构的删除时间。在时间区间外观察到的延迟记录 不会被纳入该区间；对于特定消息 ID，消息 ID 切片可能包含针对这些消息 ID 的后续删除操作。

快照（`snapshot`）固定了创建时间、日志序列/哈希边界、匹配计数、首/末 序列以及 `result_hash`。后者是按字典序排序的匹配 事件哈希的 UTF-8 规范 JSON 数组的 SHA-256 哈希值，其中空切片用 `[]` 表示。 它还包含确切的 类型计数以及一个 24 格的观测时间微型图。一个切片存储的是查询，而非重复的源 记录。导出时，`board/slices/<id>.json` 会列出当前哈希值以及新增/移除的序列。 验证器会在创建边界处重建原始结果，然后重建当前结果。 新增的记录将作为变更事实进行报告。删除原始事件会破坏不可变的 证据链；系统不会将其作为从切片中进行的普通删除而默认接受。

“反应”快照中的近期参与者列表不完整。资源管理器会比较同一聊天/消息的相邻快照 （包括切片范围外的先前快照），并报告**各观察结果之间的** 聚合计数差异。对于缺失的近期参与者，系统不会认定其已删除某条“反应”。 第一个快照没有推断出的早期状态。参与者的观察结果仍归因于 其被提供的快照，而非某个虚构的操作时间。

## API 和导出功能

`GET /api/board`接受collection/chat/author/label/state/from/to/q/kind/comments、offset/limit 以及newest/oldest排序参数。`GET /api/board/card/{id}`返回卡片、源文件预览、对话线程、 状态历史记录及相关卡片。参与者子路由返回符合条件的提及选项。 `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}`用于追加一条记录。 `POST /api/board/slice-preview`用于计算查询。切片记录通过 `GET /api/board/slice/{id}/records`进行分页；重新计算时始终使用当前稳定的读取快照。 实时 `/api/stream` 发布不含有效载荷的 `board` 通知，与日志游标独立。

`GET /api/board/export` 返回一份经过签名的文档。受聊天限制的访问权限将收到一份标注清晰的 签名**披露文件**，绝不会包含其他聊天的注释或完整对话链。完整的证据 ZIP 文件 包含 `annotations.jsonl`、经过签名的 `case-board.json` 以及切片 JSON 附录。 HTML/PDF/JSON 报告 设置可选择“无案例板”、“不含讨论的书签/片段”或“带评论的卡片”。该 部分明确区分了团队意见与观察结果。报告数据过滤器也会限制 可读笔记的内容；证据 ZIP 包中的完整签名源文件则保持完整。

`GET /api/board/slice/{id}/export` 将生成一个带签名的 `tgwitness-board-selection-v1` JSON 片段； `?format=csv` 将生成一个便于使用的表格，但不包含独立签名。保留 JSON 和 ZIP 格式：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

选择性检查用于验证签名声明、精确的源记录及其查询在指定边界处的完整性。 证据 ZIP 文件可能更新，但必须包含该前缀。若目标悬空，系统将明确报告。若原始切片快照不同、注释被修改、 重放状态不匹配或源文件被更改，则验证失败。 未带注释的旧存档 仍保留其现有的验证行为。

移交默认设置为**“不包含**”。 显式包含操作会将卡片穿插于已 简化的记录中，省略无法访问/被遗漏的目标，隐藏源文本 已被简化的高亮内容，按照相同的提及/联系人规则清理团队文本，并可选地将 元数据及笔记中已知的调查员标签替换为 R01、R02…… 不披露原始的 `annotations.jsonl`文件。已签名的`tgwitness-case-board-handover-v1`侧车文件和报告 包含相同的最小化内容。切片计数仅描述已披露的记录，原始 快照/查询参与者的详细信息被隐去。 简化工具未识别的自由文本名称仍需 进行审查，这与常规移交流程一致。此衍生文件不保证在编辑后保留原始 注释签名。

## 操作限制

参数包括 10,000 张卡片和 50,000 条评论的软限制、最多 5,000 条记录的切片页面，以及媒体预览控制。达到软限制时仅会发出警告，不会删除历史记录。 信息流页面 最多显示 200 张卡片。独立 JSON 切片摘录上限为 64 MiB；若需处理更大规模的数据，请缩小查询范围或使用 带签名的 ZIP 文件。独立验证器将注释回放上限设为 256 MiB。 Case Board 未启用也未实现任何外部评论通知功能。

该功能的自动化验收使用虚构数据和模拟的 Telegram 传输通道来 检查存储、访问、渲染和导出情况。有关证据检查范围的详细信息，请参阅[“验证范围](https://phishdestroy.github.io/TgWitness/zh/docs/reference/evidence/#verification-scope) ”。
