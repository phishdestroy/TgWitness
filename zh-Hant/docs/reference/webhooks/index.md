# 外發 Webhook

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/webhooks/

將特定範圍的事件傳送至 HTTPS 接收端，並附帶 HMAC 簽名、重試機制及傳送狀態。

[工作流程指南](https://phishdestroy.github.io/TgWitness/docs/archive/) · [維基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

在所選工作區中，開啟「**整合」→「外發 webhook」**。 新增一個 HTTPS 接收器，選擇「收集器／媒體／匯出」事件，並可選擇針對 新訊息及變更的聊天室。預設情況下不包含訊息內容。啟用摘要功能 將在訊息變更事件中最多新增 1,000 個字元；Telegram 的原始欄位及 憑證絕不會被傳送。

將 HMAC 密鑰複製一次至接收端的受保護設定中。該密鑰 已加密儲存於 TgWitness 的金庫中，且無法透過控制面板檢索。移除 並重新建立目標位置以進行輪替。**向合成**測試佇列**發送**一則 不含聊天內容的測試訊息；刷新傳送狀態以查看結果。

此傳送機制在 Apprise 的基礎上擴展現有的通知迴路。它採用 工作區的外部路由及現有的私有目的地限制。此機制 不提供直接的備用方案或後續重定向。URL 不得包含憑證、 查詢字串或片段；私有地址需啟用伺服器層級的網路 選入機制，而非面板使用者可繞過的設定。

## 有效載荷與簽名

結構：[`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json)。每個有效載荷 均包含 `event_id`、`timestamp`、`workspace`、`type`、`synthetic` 以及計數器。 基於日誌的事件包含其序列號與雜湊值。完整匯出完成及 合成測試屬於傳輸事件，不包含虛構的簽名日誌參考。 Telegram 刪除通知與 `missing_on_recheck` 仍屬不同類型。

`X-TgWitness-Signature` 標頭應為 `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`。 針對精確的位元組序列 `timestamp + "." + raw_request_body` 計算 HMAC， 並將顯示的密鑰視為 UTF-8 位元組。在解析或處理 訊息正文之前，以恆定時間比對簽名。若時間戳記與 您的系統時間相差超過五分鐘，則予以拒絕。每次傳送嘗試時， 時間戳記都會重新更新。

請將 `event_id` 作為幺半抗變換鍵儲存於持久性儲存裝置中，並在產生副作用前設定原子性唯一 約束。僅憑有效的簽名並不能防止 最近的請求被重播。請至少保留已處理的 ID 至整個 重試時段結束為止；若接收端可重新處理儲存的事件，則應保留更長時間。

## 重試

傳送作業會在 HTTP 請求前被持久化排入佇列。其採用「至少一次」 的語義：若確認回執遺失或系統重啟，可能會再次傳送具有 相同 ID 的事件。系統會進行八次嘗試，並採用指數退避機制，起始間隔為 15 秒，上限為一小時。成功傳送需獲得 2xx 狀態碼回應。 已耗盡的任務 會留下可見的錯誤訊息；重試結束後，無法保證能成功傳送。

佇列可容納 1,000 筆傳送任務。當佇列已滿時，日誌事件的掃描作業將暫停，並 在釋放出空間後恢復。 無法排入佇列的完整匯出任務 會觸發可見的佇列錯誤。每次通知傳送 最多嘗試五次，並保留最近 100 筆嘗試記錄。移除目的地 也會一併移除其待處理的傳送任務。

## n8n 範例

匯入[範例工作流程](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json)。該工作流程目前處於非活躍狀態， 且不包含任何機密資訊或下游動作。 請在 n8n 工作環境中設定 `TGWITNESS_WEBHOOK_SECRET`，允許該環境存取，並為 Code 節點啟用 `crypto` 內建功能。此範例使用 Webhook 節點的 raw-body 選項， 檢查簽名與新鮮度，並確認已驗證的事件。這與 該節點的[文件中所述實作](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts)方式相符。

在新增 SIEM 寫入或通知之前，請先建立以 `event_id` 作為鍵值的持久性冪等儲存空間。 請根據您選擇傳送的資料，限制 n8n 工作流程的編輯及執行日誌的保留期限。 TgWitness 不會新增任何傳入指令。
