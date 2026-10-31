# 一個日誌。四種收集模式。八個驗證等級。

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/guides/modes.html

模式、情境與證據等級

TgWitness 記錄已連線帳戶所觀察到的內容。第三方可透過獨立受信的金鑰，驗證該記錄的完整性。

[收集模式](https://phishdestroy.github.io/TgWitness/zh-Hant/guides/modes.html#scope)[應用情境](https://phishdestroy.github.io/TgWitness/zh-Hant/guides/modes.html#scenarios)[證據等級](https://phishdestroy.github.io/TgWitness/zh-Hant/guides/modes.html#levels)

3–5 分鐘概覽 · 虛構範例 · 現行實作

1. **Telegram**

   帳戶可見的更新
2. **收集器**

   關聯記錄，每筆均經簽署
3. **驗證者**

   可信密鑰 + 保留的邊界

`h₁ → h₂ → h₃ · Ed25519`完整性已通過驗證。Telegram 的來源與訊息的真實性仍是兩個獨立的問題。

## 選擇觀察範圍

三種範圍與一個調查預設值。排除項目與啟用的來源類型仍適用。

預設**選定的聊天室**

記錄

僅採用經人工精選的來源。

新聊天室

不會自動新增。

選擇

一組已知的頻道或群組。尚未確定任何固定的聊天容量。

**不執行** 本系統不會偵測其他聊天室，亦不會補全較早的聊天紀錄。

帳戶資料夾**Telegram 資料夾**

記錄

包含資料夾及其分類，若已設定，則排除排除項目及已歸檔的聊天室。

新聊天室

匹配活躍的聊天室；一小時內的資料夾變更。

選擇

分析師已建立案件資料夾。請確認資料是透過專用帳戶進行蒐集。

**不執行** 它不會套用資料夾的變更 muted/read 條件。

確認範圍**完整帳戶**

記錄

選定類別中，帳戶可見的聊天室，包括私人對話與機器人。

新聊天室

將於首次更新時新增。

選擇

專用的觀察帳戶，包括參與案件的帳戶。

**不執行** 它不會自動加入聊天室，也不會繞過來源存取機制。

整個帳戶預設值**調查模式**

記錄

所有來源類型、自身操作、來源檔案，以及新發現來源最近 200 則可見訊息。

新聊天室

新的聊天室或機器人將獲得一個檔案及歷史紀錄快照。

選擇

透過控制面板加入團隊或與機器人互動。檢視並儲存預設設定。

**不執行** 它不會對所有現有聊天室進行快照，也不會監測在其他客戶端按下的回調功能。

這些卡片僅供本地比對使用，並非即時收集器控制項。它們不會對帳戶造成任何變更。

**不執行** 任何模式均不得讀取秘密聊天內容、在程序停止時進行記錄、自行加入來源，或檢索超出請求範圍的早期歷史紀錄 snapshot/export.

[閱讀詳細內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/)

## 透過 GitHub Actions 擷取（預覽版）

新的 Telegram 登入工作階段、一個聊天、加密封存和 GitHub 來源證明。

[開啟擷取助手](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/capture/)

## 記錄內容

僅已傳送或明確請求的觀察記錄才會被納入紀錄。來源不明的觀察記錄將維持未知狀態。

 擷取開關 · 本地化示意圖新訊息編輯刪除內容反應會員資格

此面板會針對每個工作區套用這些設定。關閉某項設定時，現有記錄將予以保留；重新開啟該設定時，不會重建遺漏的事件。

**事件矩陣：已保存的資料與尚待釐清的未知事項**

| 類別 | 已儲存 | 仍屬未知 |
| --- | --- | --- |
| 訊息 | 文字、ID、發送者元資料、回覆上下文及原始更新封套。 | 無第三方可驗證的 Telegram 簽名。 |
| 編輯 | 所有被觀察到的版本，且不覆寫較早的版本。 | 中間的編輯可能被遺漏；發送者未必就是編輯者。 |
| 刪除 | 若可取得，請一併附上通知內容及先前儲存的文字。 | 未提供刪除者及確切的操作時間。 |
| 無範圍限制的刪除 | 帳戶層級通知；未知對等方仍會明確標示。 | 不進行猜測性聊天。關聯時，在可能的情況下會使用先前儲存的帳戶範圍內 ID。 |
| 反應 | 已傳遞的計數器與可見的近期身分。 | 並非所有反應器皆可見；若要取得完整的可用清單，需進行獨立查詢。 |
| 會員資格 | 已傳送的服務訊息與參與者更新。 | 角色與聊天類型會限制可見性；沉默並不代表不存在。 |
| 附件 | 原始版本描述符、儲存的位元組、 SHA-256 以及嘗試結果。 | 已消失的檔案可能無法取得；較新版本不會取代它。 |
| 歷史快照 | 目前可見的訊息，標記為歷史觀察記錄。 | 先前的編輯內容及已消失的內容均不予重建。 |
| 自身行為 | 發送 messages/edits 及相應的回覆鍵盤 button_press 的元資料。 | 在其他 Telegram 客戶端觸發的回呼將無法被偵測到。 |
| 機器人按鈕 | 回呼、URL、網頁應用程式及請求元資料將與訊息一併保留。 | URL 及 phone/location 請求皆為純文字，不會自動開啟或執行。 |

### 預設附件限制

照片

20 MiB

影片

100 MiB

檔案

50 MiB

動畫

20 MiB

影片筆記

50 MiB

語音

20 MiB

音訊

50 MiB

貼圖

5 MiB

**不執行** 開關功能不會刪除嵌入的元資料，也不會停用運作紀錄。擷取功能不會識別 Telegram 未提供的行為者。

[閱讀詳細內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/)

## 請僅使用您所擁有的授權

每個帳戶皆擁有專屬的工作區、日誌、簽名金鑰、路由及佇列。

### 電話號碼 + 代碼

啟用時 2FA 。

### QR code

請從授權裝置進行掃描； 2FA 可能仍需如此。

### Telethon .session

匯入該帳戶的會話檔案。

### Pyrogram .session

匯入受支援的 Pyrogram 會話格式。

### TData ZIP

僅支援一個 Desktop 帳戶；若已設定，則使用本機通行碼。

### StringSession text

貼上一個 Telethon StringSession.

### .session + .json

選擇會話及相應的相關元資料。

### 授權金鑰 HEX + DC ID

導入帳戶授權時，須一併包含其資料中心識別碼。

**API pair**

您自己的 API 配對組合為選用項目。若未提供， TgWitness 系統將使用公開配對池，其中包含來自官方 Telegram Desktop 的配對。

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy 此功能尚屬實驗性質；內建的公開 MTProxy 清單。代理路由失敗時，不會回退至直接連線。

同一台機器上的兩個工作區並不等同於兩個獨立的見證者。

**不執行** 匯入操作不會繞過 Telegram 的授權機制， 2FA 亦不支援未受支援的連線格式。帳戶仍共用同一應用程式執行程序。

[帳號格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/)

## 從控制面板進行操作

發送或回覆訊息、按下當前機器人按鈕、儲存連結預覽後，請明確加入聊天室，或透過其啟動參數啟動機器人。

`interaction.preview``interaction.requested``interaction.result`

預覽、請求及結果回執均經簽署。按下按鈕前，伺服器會再次擷取訊息，並拒絕已變更的鍵盤輸入。回傳的回呼文字與網址仍屬已記錄的上下文。

**不執行** 不包含網頁應用程式、支付功能、 phone/location 分享或內嵌查詢。顯示網址並不代表會開啟該連結。

[閱讀詳細內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/)

## 恢復與連續性

應顯示缺口，而非隱藏。

### 恢復已儲存的位置

重新啟動後，系統會向 Telegram 查詢遺漏的更新。有限的保留時間與過期的差異紀錄可能導致資料缺口。

### 重新檢查可見訊息

預設值：優先來源每 15 分鐘更新一次，其餘來源每 6 小時更新一次。結果包含 message.recovered 以及 message.missing_on_recheck.

### 閱讀 coverage.json

簽署後的匯出檔將附帶觀察期間、附有理由的缺口，以及未被觀察到的 ID。重新檢查時發現缺失的記錄，並不等同於刪除通知。

**不執行** 後續的歷史快照並不會抹除服務中斷的紀錄，亦無法復原所有消失的版本。儲存的游標並非對日誌接受情況的無損確認。

[閱讀詳細內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/)

## 七個層級。不同的問題。

每個機制皆用於解答特定範圍的問題。應分別配置外部服務，並將其信任錨點保留在收集器之外。

1. ### 記錄

   SHA-256 鏈 + Ed25519 每筆事件；首個 previous_hash 為 64 個零。

   **第三方驗證** 在固定收集器金鑰下的排序與簽名。

   **不執行** 這並不能證明其源自 Telegram 或內容完整無缺。

   **驗證指令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### 容器

   manifest.json 列出檔案雜湊值； manifest.sig 對其進行簽署。 media.saved 將附件位元組綁定至某個事件。

   **第三方驗證** 所提供的檔案與已簽署的清單及媒體收據內容一致。

   **不執行** 它不會對另行下載的 CSV, HTML 或截圖進行簽名。

   **驗證指令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### 保留的邊界

   啟動時進行檢查點備份，預設每 5 分鐘執行一次，並進行有序停止。請在其他位置保留一份副本。

   **第三方驗證** 後續的匯出內容須與先前保留的長度及頭部資訊一致；可偵測到回滾情況。

   **不執行** 它無法偵測日誌與所有保留檢查點同時被替換的情況。

   **驗證指令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### 外部時間

   證據模式會傳送一個檢查點 SHA-256 至 RFC 3161 主管機關（FreeTSA, DigiCert) 及 OpenTimestamps 行事曆。

   **第三方驗證** 經驗證的 TSA 回應會為這些位元組標記時間；經確認的 OpenTimestamps 證明則將其錨定於比特幣。

   **不執行** 它不會將已準備的請求或待處理的日曆收據視為已確認的時間戳記。

   **驗證指令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### 獨立見證人

   將主機、範圍限定唯讀端點、新挑戰及其專屬 key/journal 以及 TGW1 頻道貼文。

   **第三方驗證** 先前已接受的分支頭；狀態包括 ok、 key_changed、回滾、分叉、無效以及 no_response.

   **不執行** 這不會將同一收集器主機上的兩個工作區轉變為獨立的見證者。

   **驗證指令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### 站外副本

   S3- 相容版本，以 AES-256-GCM; Object Lock 加密的相容副本（當儲存桶支援此功能時）。

   **第三方驗證** Restore 僅在日誌、檢查點及保存媒體的驗證成功後，才會發布檔案。

   **不執行** 若未提供匯出的金鑰，則無法進行還原；若未檢查儲存回應，則不假設資料已保留。

   **驗證指令**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### 執行來源追蹤

   簽名執行收據：來源雜湊值、依賴項版本及程序上下文。由系統自行回報。

   **第三方驗證** 簽名收集器針對其自身執行所回報的內容。

   **不執行** 本系統不提供獨立的程序驗證，亦無法排除記錄前系統已遭入侵的可能性。

   **驗證指令**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### 無任何層級能證明

每則 Telegram 更新的送達；文字內容的真實性；發送者 ID 確實識別真實人士；記錄前未發生資料蒐集者遭入侵的情況；以及在法庭上的可採納性。

[獨立見證人](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/)

本地 SHA-256 實驗

### 嘗試修改記錄 2

下一筆記錄會保留先前儲存的連結。變更文字內容會改變記錄 2 的計算結果哈希值。

記錄 2 的內容

記錄 1`h1`以 64 個零開頭

記錄 2`h2`包含已儲存的 h1

記錄 3`h3`包含已儲存的 h2

靜態範例： h2 涵蓋「11:00 見面」。若變更該文字，將導致 h2；記錄 3 仍引用已儲存的 h2.

**檢查完整的摘要**

儲存紀錄 2 的雜湊值

`SHA-256(e₂)`

重新計算的第 2 筆記錄雜湊值

`SHA-256(e₂)`

此範例僅計算雜湊值，而非簽名。實際的驗證器會將每個簽名與連結與可信密鑰進行比對。

 [閱讀詳細內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/how-it-works/)

## 選擇一條穿越證據的路徑

虛構情境。請在相關事件發生前開始蒐集資料；除內容外，亦須保留其邊界與間隙。

### 頻道變更付款詳細資訊

模式 → 事件

選定的聊天室 → 訊息、編輯、刪除。

輸出

透過雜湊值記錄觀察到的貼文版本與附件。

驗證

已簽署 ZIP + 保留檢查點 + 經驗證的 TSA 回應。

**不執行** 它無法復原從未被擷取過的原始資料。

### 事件發生後，訊息將會消失

模式 → 事件

資料夾或整個帳戶 → 所有事件類別。

輸出

已儲存的原始內容、刪除通知及存在缺漏的涵蓋範圍。

驗證

簽署 ZIP + 獨立見證日誌。

**不執行** 若通知中未提供行為者資訊，則無法據此識別刪除者。

### 調查商店機器人

模式 → 事件

調查預設 → 按鈕、連結預覽及明確的機器人啟動。

輸出

簽署過的互動收據、回傳的回調函式及儲存的設定檔。

驗證

已簽署 ZIP；請根據 ZIP.

**不執行** 它不會開啟機器人網頁應用程式、進行付款，也不會記錄其他客戶端的回調。

### 參與者在不同聊天室中會更換名稱

模式 → 事件

任何範圍 → 被觀察的 sender/profile 元資料。

輸出

依數值 ID 排列的名稱／使用者名稱歷史紀錄、「亦見於」連結及提取的線索。

驗證

檔案 JSON 已與簽名版本進行比對 ZIP.

**不執行** 它不會將錢包、類似手機號碼的字串或使用者名稱轉化為經證實的身分。

### 長期觀察，並備有異地副本

模式 → 事件

任何範圍 → 證據模式及一個 S3 具備支援功能的複本 Object Lock.

輸出

加密副本、保留的檢查點及時間戳記回應。

驗證

請使用匯出的金鑰進行還原，然後在不使用原始伺服器的情況下進行驗證。

**不執行** 本文件無法取代獨立見證人或另行保留的解密金鑰。

[閱讀詳細內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/)

## 交付可驗證的套件

請提供已簽名的原始檔、獨立保存的金鑰指紋、相關檢查點以及驗證結果。

- 已簽署 ZIP
- JSONL
- CSV
- HTML
- 檢查點
- 已讀回執
- 聊天記錄匯出： chat.json / chat.html
- 檔案 JSON
- 密碼保護 AES-256 ZIP
- 針對多個帳戶分別進行匯出
- 串流 CLI：5 GiB 預設限制

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

應從可信副本中取得驗證器，而非從正在檢查的存檔中取得。

**不執行** 獨立版 CSV 與 HTML 並非簽名容器。密碼用於保護傳輸機密性，而非真實性。多次匯出不會合併帳戶日誌。

[閱讀詳細內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/)

## 請比對交付的成果

基本 artefact 未附加簽名、時間戳記或見證系統。腳本與記錄器因實作而異；「部分」意指僅限於已擷取或可見的內容。

| 方法論 | 編輯／刪除 | 簽名記錄 | 外部時間 | 獨立見證人 | 涵蓋範圍／缺漏 | 無作者的驗證 |
| --- | --- | --- | --- | --- | --- | --- |
| Telegram Desktop 匯出 | 部分 | 否 | 否 | 否 | 否 | 否 |
| Telethon 快照腳本 | 部分 | 否 | 否 | 否 | 否 | 否 |
| 刪除記錄器：文字日誌 | 部分 | 否 | 否 | 否 | 否 | 否 |
| 螢幕截圖／網頁擷取 | 部分 | 否 | 否 | 否 | 否 | 否 |
| TgWitness 附帶已配置的額外設定 | 部分 | 是 | 是 | 是 | 部分 | 是 |

**不執行** 本表格並未評估每項腳本或記錄產品。可選的時間與見證檢查需具備專屬的服務與信任錨點；其中任何一項均無法確立來源真實性。

[閱讀詳細內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/)

## 將限制與證據一併保留

當驗證範圍保持明確時，驗證才具有實用價值。

- 秘密聊天功能不可用。
- 當程序停止時，不會記錄任何內容；恢復能力受到限制。
- 經驗證的紀錄並不證明其內容屬實。
- 持有金鑰的操作者可對任意內容進行簽署。獨立見證者與時間戳記旨在限制後續內容替換，而非防止初始擷取時的欺詐行為。
- 請使用專用帳號，而非您的主要帳號。
- Telegram 可能會因請求量過大而限制帳戶。

**不執行** 任何模式或證據等級均無法確立法律上的可採納性、Telegram 訊息的完整傳送，或現實世界中的身分。

[設定指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh-Hant)[專用帳戶](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/)
