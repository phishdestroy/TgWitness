# 了解證據如何運作

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/concepts/

訊息內容可能會變更，但您所觀察到的記錄應始終可供查證。

請探索以下兩個小型實驗。它們使用虛構的訊息，全程在您的瀏覽器內運行，且絕不會連線至 Telegram。

## 一條訊息，三項觀察

當 Telegram 傳送新訊息、編輯通知或刪除通知時，收集器會分別追加三項獨立的記錄。編輯操作不會取代最初的記錄，刪除通知也不會將其刪除。

01 / 訊息流歷程說明性流程圖

Telegram delivers an update to the collector, which appends a journal record. · Telegram · 收集器 · 日誌 · 更新 → · 追加 →

當前聊天視圖 訊息 #42

訊息已刪除

該訊息已從聊天視圖中消失。

觀察日誌 3 筆記錄

1. 01

   `message.new`

   上午 10:00 見面

   ✓
2. 02

   `message.edited`

   上午 11:00 見面

   ✓
3. 03

   `message.deleted`

   關於 #42 的刪除通知

   ✓

所有三項已記錄的觀察結果均保留在日誌中。

針對已選取來源的簡化路徑。操作記錄亦會同步至真實日誌。擷取內容取決於該帳戶的可見範圍以及 Telegram 實際傳送的內容。

刪除通知既未提供可靠的刪除時間，也未指出刪除訊息的人員。保持這些數值的未知狀態，可維持「觀察」與「推測」之間的區別。

## 修改一則記錄。追蹤雜湊值。

每筆記錄皆包含前一筆記錄的雜湊值。其自身的雜湊值涵蓋事件欄位，包括該連結。由外部保留的檢查點會固定特定的日誌長度與起始雜湊值。

02 / HASH-CHAIN SANDBOX真實 SHA-256 · 記錄範例

記錄 01**已收到訊息**`h₁ = SHA-256(e₁)`連結至 64 個零

記錄 02**上午 11:00 見面**`h₂ = SHA-256(e₂)`包含 h₁

記錄 03**已偵測到刪除**`h₃ = SHA-256(e₃)`包含 h₂

另存於其他處**3 筆記錄 · 標頭 `h₃`**請將此固定邊界與提供的日誌進行比較。

修改事件會改變其雜湊值。重建鏈條會改變其起始節點。移除尾部會使其長度短於保留的檢查點。

**檢視記錄 2 及完整雜湊值**

此為本範例中經過雜湊運算的原始 UTF-8 JSON 內容。數值均為虛構；九個欄位及其序列化格式均符合日誌格式規範。

```

```

已儲存記錄 2 的雜湊值

``

重新計算的記錄 2 雜湊值

``

此沙盒僅計算雜湊值，而非簽名。真正的驗證器還會檢查每個事件的 Ed25519 簽名、序列號及連結。僅憑重建雜湊值，無法在可信密鑰下產生有效的簽名。

## 實際規則，簡要說明如下

雜湊值 + 簽名

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** 將九個事件欄位序列化為 UTF-8 JSON：鍵值按順序排列、無額外空白、無 ASCII 轉義符，且不含 NaN/無限大值。該事件的 `previous_hash` 值為 hi−1。顯示的 h0 代表 64 個零字元；簽名涵蓋 32 位元組的原始摘要。

這九個欄位分別為 `seq`、`observed_at`、`source_at`、`kind`、`chat_id`、`message_id`、`actor_id`、`payload` 及 `previous_hash`。此為 TgWitness 文件中[記載的 JSON 編碼格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#event-canonicalization)；雜湊值與簽名本身並非雜湊輸入欄位。

保留檢查點

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

請驗證固定收集器金鑰下的檢查點簽名，然後將其邊界與已驗證的日誌進行比對。後續的匯出檔可能包含更多記錄；但其內容仍須與較早的檢查點相符。

## 三個問題，三種不同的檢查方式

[01 / 完整性**這則記錄有變更嗎？** 請使用獨立的可信密鑰來驗證雜湊值與數位簽名。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/)[02 / 連續性**先前保留了哪些內容？** 將簽名過的匯出檔與由獨立見證者保存的檢查點進行比對。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)[03 / 交付**這些測試事件是否已送達？** 將各帳戶的發送、編輯及刪除操作與其對應的日誌進行比對。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/cases/)

相符的雜湊鏈可解答完整性相關問題。它並不能證明 Telegram 訊息已完整送達、訊息內容屬實，亦無法確立獨立可信的觀察時間。

追蹤從帳戶取得到案件檔案編製的[完整調查](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/cases/)過程。
