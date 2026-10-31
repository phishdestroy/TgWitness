# 瀏覽檔案庫

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/archive/

尋找訊息。查證來源。建立案情。

這些工具可從當前主分支取得。0.7.0 便攜版預覽版早於這些工具；若要使用此工作流程，請從原始碼檢出。

01**導入歷史紀錄**

將已啟用的來源中的過往訊息載入至工作區。

02**追蹤消息來源**

搜尋存檔，並開啟每個搜尋結果對應的已儲存訊息。

03**確保交接流程清晰明確**

請將您的分析結果另行儲存，並將其旁附的簽名證據一併匯出。

擷取的紀錄、辨識出的文字與分析師的結論均保持獨立分明。

## 載入過往訊息

1. 開啟「**開放來源」（**Open **Sources）**，檢視已啟用的聊天室並開始監測。
2. 選擇「**載入完整歷史紀錄**」。執行時將使用當下選取的來源清單。
3. 請視需要使用「**暫停歷史紀錄」**與「**繼續歷史紀錄」**功能。重新啟動後，請明確地恢復操作。
4. 檢查各來源的結果及附件佇列。將已簽名的進度報告與證據匯出檔案一併儲存。

此操作會將可用訊息填滿工作區。按聊天室進行的 HTML/JSON 匯出則屬另一項獨立操作。[歷史紀錄與資料復原詳情](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/history/)。

## 先搜尋，再決定是否使用 AI

1. 開啟**「查詢存檔」功能**。選擇工作區、聊天室及監測期間。
2. 搜尋短語、網域或訊息 ID。開啟符合條件的記錄及其儲存的版本。
3. 進行 AI 分析時，管理員需先設定服務供應商。審閱**傳送至模型的資料**，並在批准請求前取消勾選不需要的片段。
4. 請檢查回傳的引用資料。將答案儲存為報告，並加入您自己的修訂或註解。

搜尋功能在本地執行，不使用人工智慧。分析報告會保留來源參考與修訂歷史紀錄；這些報告與簽名日誌是分開儲存的。[服務提供者設定與報告](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/analysis/)。

## 選擇您所需的連線方式

| 任務 | 開啟 | 設定 |
| --- | --- | --- |
| 閱讀來自 AI 客戶端的精選聊天記錄 | **整合功能 → MCP** | [安裝 MCP 擴充套件、發行範圍限定憑證，並連接客戶端](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/) |
| 識別儲存媒體中的文字 | `media.saved` 記錄 → **識別附件** | [設定本機 Docker 工作節點及所需的語言／模型檔案](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/media-analysis/) |
| 將事件傳送至 n8n 或 SIEM | **整合功能 → 外發 webhook** | [新增接收者、驗證 HMAC 並對事件 ID 進行去重](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/webhooks/) |

**哪些存取憑證該放在哪裡？**

控制面板存取權限僅限於案件審查人員。MCP 連線者將獲得獨立的唯讀存檔憑證。Webhook 接收器使用其專屬的 HMAC 密鑰。所有使用者均無需 Telegram 會話檔案。

[分享控制面板存取權限](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/access/)或[設定 MCP 客戶端](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/)。

## 提供資料來源與結論

請將經審核的分析報告與簽署過的證據 ZIP 檔一併保存。該報告闡述您對來源資料的解讀；ZIP 檔則讓收件者能透過獨立可信的指紋與檢查點，核對儲存的紀錄是否正確。

[匯出與驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/) · [完整調查流程指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/cases/)
