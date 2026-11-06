# Telegram · 设计报告

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reports/

让读者从案件问题直接到达保存的记录。

Report studio 汇总您挑选的数据、变更历史、图表和您的发现。八种设计，HTML 和原生 PDF。每份 HTML、PDF 和 JSON 报告都用您的密钥封印。

## 三步生成报告

1. **导出 → 配置和预览 → 数据**：整个工作区，或选择聊天、作者、日期（UTC，即 TgWitness 看到记录的时间）和记录类型。
2. **设计与内容**：选择设计和要包含的内容：图表、参与者、聊天记录、变更、Case Board 条目、您的案件详情和笔记。
3. **预览**：检查数量、活动、样本和缺失的 ID 范围。保存，然后下载所需格式。

### 为读者整理相同的保存材料

合成示例 · 示意图布局，并非生成的报告

1. **选择。**为该案件选择两个聊天记录及观察时间段。
2. **撰写内容。**选择布局，并选定能回答该问题的章节。
3. **预览。**请核对选定字数及保存的“修改前”与“修改后”文本。
4. **验证。**生成最终文件，并将其签名与可信工作区的指纹进行比对。

#### 选定要点

2 次聊天 · 1 天观察期

消息、编辑及删除通知

#### 报告结构

##### 更改了付款目的地

案件问题 → 范围 → 调查结果 → 记录引用

**消息背景**

观察项 #142：“请使用新的支付链接。”

**已保存的更改**

译前：old.example.invalid → 译后：new.example.invalid

#### 审阅选定内容

18 条意见 · 2 次保存的编辑

发送、编辑和查看时间各有独立的标签。

#### 最终交付物

签名 PDF + 签名 JSON，或包含可读报告的签名 ZIP 文件

接收方需核对文件及可信指纹。

## 选择阅读风格

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**：相同的记录，不同的外观。切换时保留您的选择和笔记。可用 25 种语言中的任意一种。

PDF 使用内置字体生成，无需浏览器。中文、日文和韩文需要服务器上有 Noto Sans CJK 之类的字体（系统级或位于 `TGWITNESS_FONT_DIR`），否则只能得到 HTML 和 JSON。

## 结合上下文阅读变更内容

编辑显示前后对比，删除显示最后保存的版本。回复、转发、表情回应、按钮和附件都保留其引用。

设计预览使用前 50,000 条记录，数据预览精确统计全部内容。要查看最终页面布局，请生成 PDF。

## 请审慎选择受众版本

筛选只影响报告，证据 ZIP 仍包含完整日志和文件。如果接收方应得到更少，请使用[精简移交](https://phishdestroy.github.io/TgWitness/zh/docs/handover/)。更多：[报告内容](https://phishdestroy.github.io/TgWitness/zh/docs/reference/case-reports/)，[验证导出](https://phishdestroy.github.io/TgWitness/zh/docs/exports/)。
