# Telegram · 找出問題所在

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/troubleshooting/

從症狀著手，一次檢查一項。

## 控制面板要求輸入代幣

它要的是啟動器所印出檔案中的面板權杖。Docker：`docker compose exec tgwitness cat /data/panel-token.txt`。不是 Telegram 驗證碼，不是機器人權杖，也不是見證人權杖。

## Telegram 無法連線

執行連線檢查。若使用公開代理，換一個並儲存。檢查代理類型和密鑰格式。重新整理清單本身不會切換路由。

## 已連線，但無新訊息

1. 觀察是否正在執行，且在正確的工作區中？
2. 來源是否已選取，且該帳戶看得到？
3. 在測試群組中傳送一則獨特的訊息，然後搜尋它。
4. 在日誌中尋找中斷或 Telegram 錯誤。

安靜的聊天室只是沒有新內容。若完整性很重要，請執行受控的送達測試。

## 重啟後出現 FloodWait 或間隔

FloodWait 是 Telegram 在說「慢一點」。請等它過去並減輕負載，重新連線沒有用。重新啟動後 TgWitness 會補上 Telegram 仍保留的內容；其餘的是空缺，請記錄下來。

## 該機器人已設定完成，但尚未發布任何內容

見證人是否正在執行，機器人能否在頻道中發文，它能否連到收集器和 Bot API？在它的日誌中尋找發文失敗。收集器端出現輪詢並不代表貼文已送出。

## GitHub 憑證整合功能在哪裡？

**規劃中。**「額外資訊」部分說明了擬議的分叉與建置驗證工作流程。目前尚無 GitHub 憑證表單，亦無自動驗證機制可確認運行中的安裝環境是否與儲存庫相符。請參閱[當前功能狀態](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/)。

回報 bug？請提供版本、作業系統、步驟和去除個資的錯誤訊息。切勿在公開 issue 中放入工作階段、權杖、私人訊息或資料目錄。
