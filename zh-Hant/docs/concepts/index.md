# 了解證據如何運作

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/concepts/

訊息會變。您對所見內容的紀錄不該改變，而且任何人都應該能核對這一點。

下面是兩個小實驗。訊息是虛構的，一切都在您的瀏覽器中執行，不會傳送到 Telegram。

## 從聊天記錄匯出到可驗證的紀錄

[Telegram Desktop 匯出](https://telegram.org/blog/export-and-more)將目前可見的歷史儲存為 HTML 或 JSON。TgWitness 增加了持續的變更日誌、每筆紀錄的簽名，以及他人可以對照的檢查點。

| 任務 | Telegram 桌面版匯出 | TgWitness |
| --- | --- | --- |
| 閱讀已儲存的對話 | HTML 或 JSON 格式，並包含選定的媒體檔案 | 已儲存的聊天紀錄、可搜尋的日誌及離線報告 |
| 追蹤隨時間的變化 | 匯出時可用的歷史紀錄 | 舊版本、後續編輯和刪除，全部保留 |
| 交接後請檢查檔案 | 標準的 HTML/JSON 匯出檔案均未簽名 | 簽名清單、簽名紀錄和封印報告，以可信任的金鑰核對 |
| 與先前保留的狀態進行比對 | 請另行保留一份參考副本或雜湊值 | 已簽署的檢查點、獨立的見證者及可選的外部時間戳記 |

本比較依據截至 2026 年 11 月 2 日的 [Telegram Desktop 匯出程式碼](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output)。

## 一條訊息，三項觀察

一則新訊息、一次編輯和一次刪除會成為三筆獨立的紀錄。編輯不會覆寫第一筆，刪除也不會抹去它。

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

Telegram 不會告訴您是誰刪除了訊息，也不會告訴確切時間。TgWitness 將這些欄位留空，而不是去猜測。

## 修改一則記錄。追蹤雜湊值。

每筆紀錄都包含前一筆的雜湊。存放在別處的檢查點固定了日誌長度和最後一個雜湊。

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

**C** 是以 UTF-8 JSON 表示的九個事件欄位：鍵已排序，無多餘空白，無 ASCII 跳脫，無 NaN/無限大。`previous_hash` 是 hi−1，h0 是 64 個零，簽名涵蓋 32 位元組的原始摘要。

欄位：`seq`、`observed_at`、`source_at`、`kind`、`chat_id`、`message_id`、`actor_id`、`payload`、`previous_hash`。完整規格：[事件編碼](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#event-canonicalization)。

保留檢查點

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

用固定的金鑰檢查檢查點簽名，然後與日誌比較。之後的匯出可以更長，但在檢查點處必須一致。

## 三個問題，三種不同的檢查方式

[01 / 完整性**這則記錄有變更嗎？** 以您信任的金鑰核對雜湊和簽名。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/)[02 / 連續性**先前保留了哪些內容？** 將匯出與見證人保存的檢查點比較。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)[03 / 交付**這些測試事件是否已送達？** 傳送、編輯和刪除測試訊息，看看每個帳戶捕捉到什麼。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/cases/)

簽名回答「是否被改過」，檢查點回答「是否與先前一致」，測試訊息回答「我們是否全部捕捉到」。[驗證能證明什麼、不能證明什麼。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope)

下一步：從開始到案件包的[整個帳戶調查](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/cases/)。

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
