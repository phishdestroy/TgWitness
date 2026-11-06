# Telegram · 選擇代理伺服器

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/proxies/

保持帳戶上線，並由您自己決定它是否可以顯示伺服器的 IP。

## 請先選擇 IP 模式

01**隱藏網址**

僅使用代理。如果都無法使用，就等待。

02**直接作為最後手段**

延遲後直接連線，一旦有代理可用就切回代理。

03**伺服器需透過隧道或 VPN 連線**

可以直接連線。它不會替您設定或檢查 VPN。

路徑決定連線方式。IP 模式決定是否允許直接連線。

## 讓池來維護路徑

1. **帳戶 → 設定 → 連線設定**。
2. 選擇 IP 模式和**自動 MTProxy**，或固定路由。
3. 儲存，然後**測試 Telegram 連線**（登入前也能用）。
4. 開始收集，並傳一則測試訊息給自己。

新工作區預設使用自動 MTProxy 並開啟**隱藏網址**。代理池會拉取四個公開清單，檢查伺服器，保留好用的，替換失效的。

## 請使用您自己的代理伺服器

SOCKS5、HTTP CONNECT、Telegram 代理連結或營運方目錄。切換前請暫停觀察。Fake TLS 密鑰（`ee`…）無法使用。

**輪替、分享與重試設定**

**參數 → 自動 MTProxy**：失敗門檻、冷卻時間、輪替、每個代理的帳戶數。上限為 1 表示帳戶寧可等待也不共用。不同的代理仍可能共用同一個出口 IP。

## 將 Telegram 與外部請求區分開來

MTProxy 只承載 Telegram 流量。時間戳記、通知、副本和程式碼檢查走另外的 SOCKS5/HTTP 代理、帳戶的 SOCKS5/HTTP 路由，或在模式允許時直接連線。也可以關閉它們。

`TGWITNESS_PROXY_FEED_PROXY` 設定下載清單所用的路由。[見證人](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)有自己的設定。這些都不會影響您的瀏覽器或系統網路。

更多：[模式和預設值](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/#ip-modes)，[誰可以變更路由](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/access/)。
