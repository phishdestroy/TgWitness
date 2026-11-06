# Telegram · 瀏覽檔案庫

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/archive/

尋找訊息。查證來源。建立案情。

01**導入歷史紀錄**

將已啟用來源的過往訊息拉進工作區。

02**追蹤消息來源**

搜尋，然後開啟每筆結果背後保存的訊息。

03**確保交接流程清晰明確**

您的分析放在一個檔案裡，簽名證據放在旁邊。

擷取的紀錄、辨識出的文字與分析師的結論均保持獨立分明。

## 載入過往訊息

1. **來源 → 範圍內的聊天室**：檢查已啟用的聊天室，開始觀察。
2. **載入完整歷史紀錄**。它依照當下的來源清單執行。
3. 隨時可以**暫停歷史紀錄** / **繼續歷史紀錄**。重新啟動後請手動繼續。
4. 檢查每個來源的結果和下載佇列，將簽名進度報告與匯出一起保存。

這會填滿工作區。單一聊天室的 HTML/JSON 匯出是另一回事。[詳細資訊](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/history/)。

## 先搜尋，再決定是否使用 AI

1. **日誌**在本機搜尋，可依來源和時間篩選。
2. 搜尋片語或網域，開啟紀錄及其各個版本。
3. 使用 AI 時，由管理員在**整合功能**中設定服務商。然後**查詢檔案庫**：選擇聊天室和期間，查看**傳送至模型的資料**，取消勾選不該送出的內容。
4. 檢查引用，將回答儲存為報告，加上您的筆記。

搜尋不需要 AI。報告保存自己的來源和修訂版本，與簽名日誌分開。[服務商設定](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/analysis/)。

## 選擇您所需的連線方式

| 任務 | 開啟 | 設定 |
| --- | --- | --- |
| 讓 AI 用戶端讀取選定的聊天室 | **整合功能 → MCP** | [安裝 MCP、建立限定範圍的權杖並連線](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/) |
| 識別儲存媒體中的文字 | `media.saved` 記錄 → **識別附件** | [設定本機 Docker worker](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/media-analysis/) |
| 將事件傳送至 n8n 或 SIEM | **整合功能 → 外發 webhook** | [新增接收端、驗證 HMAC、去除重複 ID](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/webhooks/) |

**哪些存取憑證該放在哪裡？**

面板存取是給人用的。MCP 有自己的唯讀權杖，webhook 有自己的 HMAC 密鑰。它們都不需要 Telegram 工作階段。

[分享控制面板存取權限](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/access/)或[設定 MCP 客戶端](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/)。

## 提供資料來源與結論

請將報告放在簽名 ZIP 旁邊。報告是您對來源的解讀，ZIP 才是接收方要驗證的內容。

[匯出與驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/) · [完整調查流程指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/cases/)
