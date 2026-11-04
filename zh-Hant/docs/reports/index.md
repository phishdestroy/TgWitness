# 設計報告

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reports/

讓讀者從案件問題直接到達保存的紀錄。

Report studio 彙整您挑選的資料、變更歷史、圖表和您的發現。八種設計，HTML 和原生 PDF。每份 HTML、PDF 和 JSON 報告都以您的金鑰封印。

## 三步驟建立報告

1. **匯出 → 設定與預覽 → 資料**：整個工作區，或選擇聊天室、作者、日期（UTC，即 TgWitness 看到紀錄的時間）和紀錄類型。
2. **設計與內容**：選擇設計和要放入的內容：圖表、參與者、對話紀錄、變更、Case Board 項目、您的案件細節和筆記。
3. **預覽**：檢查數量、活動、樣本和缺少的 ID 範圍。儲存，然後下載所需格式。

### 請將相同的儲存資料以適合讀者閱讀的方式進行整理

合成範例 · 示意性佈局，並非實際生成的報告

1. **「選取」。**請為本案選擇兩個聊天室及觀察期間。
2. **撰寫內容。**選擇版面配置，並挑選能回答問題的段落。
3. **預覽。**請檢視選取的字數統計及已儲存的「前後對照」文字。
4. **驗證。**生成最終檔案，並將其簽名與可信工作區的指紋進行比對。

#### 精選觀察要點

2 則聊天紀錄 · 1 天觀察期

訊息、編輯及刪除通知

#### 報告結構

##### 付款目的地已變更

案件問題 → 範圍 → 調查結果 → 記錄參考

**訊息背景**

觀察點 #142：「請使用新的付款連結。」

**已儲存的變更**

原文：old.example.invalid → 譯文：new.example.invalid

#### 檢視選項

18 項觀察 · 2 次儲存的編輯

「發送時間」、「編輯時間」和「查看時間」各有獨立標籤。

#### 最終交付成果

簽署過的 PDF + 簽署過的 JSON，或包含可讀報告的簽署 ZIP 檔案

收件者需核對檔案及可信指紋。

## 選擇閱讀風格

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**：相同的紀錄，不同的外觀。切換時保留您的選擇和筆記。可使用 25 種語言中的任一種。

PDF 以內建字型產生，不需要瀏覽器。中文、日文和韓文需要伺服器上有 Noto Sans CJK 之類的字型（系統層級或位於 `TGWITNESS_FONT_DIR`），否則只能得到 HTML 和 JSON。

## 請在上下文中理解變更內容

編輯會顯示前後對照，刪除會顯示最後保存的版本。回覆、轉傳、表情回應、按鈕和附件都保留其參照。

設計預覽使用前 50,000 筆紀錄，資料預覽則精確計算全部。若要查看最終頁面版面，請產生 PDF。

## 請審慎選擇受眾版本

篩選只影響報告，證據 ZIP 仍包含完整日誌和檔案。若接收方應得到更少，請使用[精簡移交](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/handover/)。更多：[報告內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-reports/)，[驗證匯出](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/)。
