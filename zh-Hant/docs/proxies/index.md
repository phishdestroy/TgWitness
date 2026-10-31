# 選擇代理伺服器

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/proxies/

請保持帳戶連線。明確決定何時其路由可使用伺服器的位址。

## 請先選擇 IP 模式

01**隱藏 IP**

請使用代理伺服器。若所有代理伺服器均無法連線，請在未直接連線至 Telegram 的情況下耐心等待。

02**允許備用方案**

在設定的延遲時間過後允許直接連線；當有代理伺服器回應時，則切換回可用的代理伺服器。

03**隧道 / VPN**

允許透過主機網路建立直接連線。此選項不會安裝或驗證 VPN。

路徑決定連線方式。IP 模式決定是否允許直接連線。

## 讓池來維護路徑

1. 開啟**帳戶 → 設定 → 連線設定**。
2. 請選擇 IP 模式與「**自動 MTProxy**」，或輸入固定路由。
3. 儲存並執行「**測試 Telegram 連線」**。此功能在登入前亦可運作。
4. 開始收集後，請確認一則受控訊息已成功寫入日誌。

新的工作區採用具備「隱藏 IP」功能的自動 MTProxy。該代理池整合了四個公開來源，會檢測條目、保留可用的路徑，並替換失效的代理。下載失敗時，系統會保留先前的快照。

## 請使用您自己的代理伺服器

請輸入 SOCKS5 或 HTTP CONNECT 設定資料、貼上受支援的 Telegram 代理伺服器連結，或提供營運商目錄。在變更現行路由前，請先暫停監測。以 `ee` 開頭的偽造 TLS MTProxy 密鑰目前仍不支援。

**輪替、分享與重試設定**

在**「參數」→「自動 MTProxy」**中，設定失敗閾值、冷卻時間、預定輪替頻率以及每個代理伺服器的帳戶數量。若共享限制設為「1」，當無專用入口可用時，該帳戶將進入等待狀態。清單刷新與探測間隔將遵循主工作區的設定值。使用獨立代理伺服器並不保證會獲得獨立的出口 IP 位址。

## 將 Telegram 與外部請求區分開來

MTProxy 僅傳輸 Telegram 流量。時間戳記、通知、副本及來源驗證則使用獨立的 SOCKS5/HTTP 代理伺服器、該帳戶的 SOCKS5/HTTP 路由，或在 IP 模式允許的情況下使用 Direct 連線。這些外部請求可被停用。

明確的 ``TGWITNESS_PROXY_FEED_PROXY`` 參數用於設定資料擷取器的路由。[獨立見證器](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)會保留其自身的設定。這些控制項不會安裝系統 VPN，也不會重定向瀏覽器流量。

查看[所有模式、預設值及來源清單](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/#ip-modes)，或[選擇哪些人可以變更帳戶的路由](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/access/)。
