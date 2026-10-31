# 完整參考資料

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/

本專案的所有文件，連同其圖表均於此處呈現。指南僅為簡要指引；這些頁面則詳盡記載了所有細節。

## 設定

[### 快速入門 安裝與啟動 TgWitness 的各種方式：Windows 套件、Python、Docker 以及合成示範，並包含初步檢查步驟。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/quickstart/)[### 帳戶與會話格式 可透過手機、QR 碼或授權金鑰登入，匯入 Telethon、Pyrogram 或 Telegram Desktop 的會話紀錄，並同時管理多個帳戶。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/)[### 存取與權限 針對帳戶和聊天室設定權限範圍、選擇權限、限制連線數與 IP 位址，並撤銷存取權限。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/)[### 連線、代理伺服器與資料保護 驗證、自動代理伺服器池、IP 模式、備用策略、外部請求及機密資料儲存。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/)[### 部署 可在 Windows、Linux、macOS 或 Docker 環境中，透過 HTTPS 運行 TgWitness 服務，並具備備份與更新功能。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/)

## 收集

[### 資料蒐集原理 觀察範圍、即時更新、重新核對、附件、使用者操作以及「缺口」的含義，皆以逐筆記錄的方式呈現。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/)[### 載入來源歷史紀錄 從已啟用的來源載入過往訊息、暫停與恢復操作，並驗證經簽署的進度報告。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/history/)[### 工作流程與操作 控制面板的日常操作：運作模式、監控類別、參數、通知、匯出、備份及容量。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/operations/)[### 調查模式 涵蓋頻道、群組、私人聊天及機器人的完整帳戶調查，從調查範圍到經核實的案件檔案包。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/)[### 功能與限制 TgWitness 目前已實現的功能、Telegram 平台的限制，以及未來尚待完成的工作。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/)

## 存檔與整合功能

[### 檔案分析 搜尋已儲存的訊息、檢視 AI 輸入內容，並保存附有來源參考的分析報告。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/analysis/)[### 唯讀 MCP 將 MCP 客戶端連接到選定的工作區和聊天室，並賦予其具有有效期限且可撤銷的存取權限。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/)[### 本地 OCR 與文字轉錄 透過本地工作程序識別擷取的圖像與音訊；並將衍生的文字與其原始檔案保持關聯。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/media-analysis/)[### 外發 Webhook 將特定範圍的事件傳送至 HTTPS 接收端，並附帶 HMAC 簽名、重試機制及傳送狀態。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/webhooks/)

## 證據

[### 證據的運作方式 文中以驗證者實際使用的精確公式，詳盡闡述了雜湊鏈、簽名、檢查點及見證者的運作原理。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/how-it-works/)[### 證據格式 簽名 ZIP 檔案的內容、記錄類型、處理回執、使用者檔案、異地備份及離線驗證。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/)[### 獨立見證人 請使用具備專屬金鑰與機器人的「Witness」執行程序，將簽署過的檢查點發佈至頻道，並據此核對匯出資料。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/)[### 時間戳記 簽名檢查點的 RFC 3161 時間戳記：傳送至授權機構的內容，以及如何驗證回應。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/timestamp/)

## 安全性與專案

[### 安全性與資料處理 威脅模型、存取模型、靜態機密資料、網路暴露風險、會話匯入，以及如何回報漏洞。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/)[### 架構 說明收集器、控制面板、日誌、工作節點及見證節點等組件，以及資料在這些組件間的流動方式。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/architecture/)[### 已測試的內容 Telegram 即時測試、自動化檢查、瀏覽器檢查，以及尚未經核實的內容。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/)[### 授權說明及架構不相容聲明 TgWitness 採用 MIT 授權，供所有人使用，並說明其為何在架構上與 Taylor Wessing 的工作流程不相容。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/license/)[### 操作員不相容通知 關於 Taylor Wessing 及其來源記錄的操作員公告。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/notice/)[### 更新紀錄 按版本列出所有變更，包含尚未發布的變更。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/changelog/)
