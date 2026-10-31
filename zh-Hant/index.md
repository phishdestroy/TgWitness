# 訊息會改變。保留您所見的內容。

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/

[開源 / v0.7.0](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/changelog/)

擷取 Telegram 訊息、保存其變更紀錄，並匯出經簽署的紀錄。

[開啟示範版](https://phishdestroy.github.io/TgWitness/demo/?lang=zh-Hant)[設定指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh-Hant)

此示範使用虛構資料。無需登入 Telegram 帳戶。

 [透過 GitHub Actions 擷取（預覽版）](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/capture/) [S3 異地備份：設定與還原](https://phishdestroy.github.io/TgWitness/zh-Hant/#s3)

一則跨越時空的訊息 #0042

Northstar · 研究虛構來源／訊息 42

1. **觀察到的訊息**09:41:02

   簡報內容自 14:00 開始。
2. **編輯記錄已保留**09:43:18

   簡報內容自 15:00 開始。

   保留前一版本
3. **刪除通知**10:06:45

   擷取的內容將保留在您的日誌中。

三項觀察。一段歷史。範例

訊息雖已消失，但被擷取的歷史紀錄依然存在。

## 每項被擷取的變更。就在您需要的地方。

透過虛構的示範資料瀏覽介面。

TgWitness / 已儲存的聊天記錄您的觀察工作區

![以深色主題儲存 Telegram 對話，並將擷取的編輯內容與已刪除訊息完整保留於對話脈絡中](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / 已儲存的聊天記錄 熟悉的對話檢視介面，訊息旁會顯示已擷取的編輯紀錄及刪除通知。

TgWitness / 日誌本地工作區

![包含已觀察到的訊息、編輯紀錄、刪除通知及涵蓋事件的日誌](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / 日誌：您帳戶所記錄內容的可搜尋時間軸，包含中斷情況。

TgWitness / 編輯歷史本地工作區

![透過詳細抽屜介面，比較訊息的原始版本與編輯後版本](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / 編輯歷史 比較已擷取的版本，同時不會覆寫先前的記錄。

TgWitness / 簽名輸出檔本地工作區

![工作區匯出功能提供簽名過的 ZIP、JSONL、CSV 檔案，以及離線 HTML 報告](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / 簽名輸出 將日誌隨身攜帶，附有清單及獨立驗證者。

01 / 擷取

### 範圍由您決定。

可選擇特定聊天室、Telegram 資料夾或整個帳戶。每個帳戶皆設有獨立的工作區。

[比較資料蒐集模式](https://phishdestroy.github.io/TgWitness/zh-Hant/guides/modes.html#scope)

02 / 保存

### 變更內容將豐富這則報導。

擷取的訊息版本、刪除通知及監測缺口均會保留在日誌中。

[請參閱事件矩陣](https://phishdestroy.github.io/TgWitness/zh-Hant/guides/modes.html#events)

03 / 移交

### 一份隨行而行的紀錄。

簽名 ZIP 檔案、完整保留的檔案以及離線報告。可選配密碼保護功能。

[匯出並驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/)

## 只要改變一個位元組，區塊鏈就會告訴你。

每個事件皆連結至前一個雜湊值，並附有 Ed25519 數位簽名。

![擷取的事件會連結至先前產生的雜湊值、附帶簽名，並以可驗證的格式進行匯出。](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![若修改已擷取的記錄，將改變其雜湊值，並導致相關記錄的驗證失效。](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![透過獨立保存的檢查點，收件者可將匯出的日誌與先前的觀察記錄進行比對。](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

了解每種驗證機制能達成什麼，以及其局限性何在。

[探索八個證據等級](https://phishdestroy.github.io/TgWitness/zh-Hant/guides/modes.html#levels)

## 歡迎其他同儕審閱。

將觀察結果、檔案及離線 HTML 報告整合為單一簽名封包一併交付。

[閱讀證據模型](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/)

tgwitness-evidence.zip簽名套件

- 01

  原始觀察結果JSONL 記錄 + CSV 表格
- 02

  易讀的背景說明離線 HTML 報告 + 完整保留的媒體檔案
- 03

  獨立驗證簽名清單 + 獨立驗證器

簽名是根據可信密鑰來偵測篡改行為。簽名無法證明訊息源自 Telegram，亦無法保證完整擷取。日誌內容及媒體檔案需由您自行提供加密儲存空間。

## S3 備份。外部驗證。

保留加密副本並加入獨立核查機制。

預設為關閉狀態

### 將所有內容複製到 S3 相容儲存空間

日誌、檔案、帶時間戳記的檢查點及聊天記錄匯出檔——在上傳至 AWS S3 或相容儲存空間前均已加密。

**儲存設定與資料復原**

客戶端加密

`AES-256-GCM` 會對本機器上的物件進行加密。服務提供者會接收這些加密物件。

排程或手動備份

立即複製，或選擇 1 至 1,440 分鐘之間的間隔。請在面板中查看進度。

Object Lock

若儲存桶支援此功能，請選擇保留天數及模式。該面板會顯示上傳物件的保留狀態是否已確認。

經驗證的資料復原

請下載加密金鑰並另行保存。請在另一台機器上進行還原；檔案僅在驗證通過後才會發布。

![完整的異地複製設定面板：終端點、區域、儲存桶、存取金鑰、排程、物件鎖定及復原金鑰控制](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

已展開包含進階選項的完整控制面板。畫面中未顯示任何儲存憑證。

期刊與媒體`AES-256-GCM`相容於 S3 的儲存空間

[設定 S3 並還原副本](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3)[閱讀驗證詳情](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#off-site-copy-and-restore-s3)

**無法** 若未持有已匯出的解密金鑰，本工具無法還原訊息，亦無法取代獨立證人。

### 通知 · Apprise

透過 Apprise 接收問題警示、聊天記錄變更及每日摘要：可透過即時通訊軟體、電子郵件或您自訂的 JSON Webhook 接收。

**不執行** 除非您啟用摘錄功能，否則不會傳送訊息內容。

 [設定通知接收端點](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/operations/#notifications)

### 外部時間戳記

採用 RFC 3161 及 OpenTimestamps 進行時間戳記檢查點雜湊運算。

**不將**待處理的日曆收據視為已確認的比特幣時間戳記。

 [查看時間戳記證明](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/timestamp/)

### 獨立見證人

另有一台獨立伺服器負責儲存經簽名的觀察記錄，並可發布 `TGW1` 檢查點。

**無法做到：**它無法將同一收集器主機上的兩個工作區轉變為獨立的證據來源。

 [設定一個 Witness](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)

### 資料復原與可見的缺口

重新啟動後恢復運作。重新檢查及 `coverage.json` 顯示已恢復的訊息與遺漏部分。

**無法做到**：本工具無法還原所有遺漏的編輯紀錄或已消失的訊息。

 [檢查連續性與缺口](https://phishdestroy.github.io/TgWitness/zh-Hant/guides/modes.html#continuity)

## 您的第一個工作區就從這裡開始。

請先瀏覽示範版本。準備就緒後，請連結專用帳戶。支援 Windows、Linux、macOS 或 Docker。

[閱讀設定指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh-Hant)

**一個已匯入的會話，一個正在運行的客戶端。**

請勿同時在 Telegram Desktop 和 TgWitness 中執行已匯入的 TData／會話金鑰。Telegram 可能會使共享授權失效（AUTH_KEY_DUPLICATED）。若需並行使用，請透過手機號碼或 QR 碼建立獨立的 TgWitness 登入帳號。

[閱讀會話匯入警告](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh-Hant#session-warning)

**連線前請先瀏覽此網站。**

無需 Telegram 帳號，即可試用此虛構工作區。

[開啟線上示範 →](https://phishdestroy.github.io/TgWitness/demo/?lang=zh-Hant)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**本地安裝指令**

步驟 01

### 取得原始碼。

[請下載原始碼 ZIP](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) 檔案並解壓縮，或克隆此儲存庫：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

執行原始程式需 Python 3.11 以上版本。若系統未安裝 Python，Windows 啟動程式將提供安裝選項。

[瀏覽版本](https://github.com/phishdestroy/TgWitness/releases)

Windows 上沒有 Python？[請下載可攜式套件](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip)，解壓縮後雙擊 `TgWitness.cmd`。

步驟 02

### 選擇運行方式。

雙擊 `Start.cmd`，或在 PowerShell 中執行：

```
.\Start.cmd
```

只是想試試看嗎？雙擊 `scripts\Demo.cmd` 即可體驗獨立演示版本。無需登入 Telegram。

若已安裝 Python 3.11 以上版本及 `venv`：

```
sh start.sh
```

若要開啟虛構的日誌，請執行 `sh start.sh --demo`。

在已運行 Docker 並安裝 Compose 2.20+ 的情況下：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

第二條指令會顯示您的私人面板代幣。請將其保留在您的裝置上。

啟動後，請開啟 [127.0.0.1:8787 並輸入](http://127.0.0.1:8787)。

若透過原始碼安裝，代幣位於 `data/live/panel-token.txt`。Telegram 登入可使用內建的 API 設定，或您從 [my.telegram.org](https://my.telegram.org) 取得的專屬金鑰對。[完整設定指南 ↗](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/quickstart/)

**TgWitness 0.7.0** [最新動態 →](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/changelog/) · [功能與已知限制 →](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/)

## 清晰的操作指引。實用的下一步建議。

[探索指南 ↗](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/)

[### 模式、情境與證據等級 四種蒐集模式。八種驗證等級。為您的案件找到合適的工作流程。](https://phishdestroy.github.io/TgWitness/zh-Hant/guides/modes.html)

[01 ### 連結帳戶 支援透過手機、QR 碼及相容的會話進行資料匯入。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/accounts/)[02 ### 選擇代理伺服器 公開的 MTProxy 清單或您自訂的路由。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/proxies/)[03 ### 設定 Witness 機器人 您 Telegram 頻道中的簽名檢查點。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)[04 ### 匯出與驗證 分享擷取的歷史紀錄並驗證其完整性。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/)

## 查閱存檔。

載入歷史紀錄、檢視 AI 來源、連接 MCP 客戶端、識別已儲存的媒體檔案，並發送經簽名的 webhook。

可從當前來源取得。0.7.0 便攜版預覽版早於這些工具推出。

[探索工作流程](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/archive/)

## 開始之前。

**此頁面是否與 Telegram 相關？**

不，這是一個包含虛構範例與螢幕截圖的靜態專案頁面。實際應用程式運行於您的電腦或伺服器上；登入程序亦在該處進行。

**它能否恢復在擷取前已被刪除的訊息？**

不。TgWitness 僅保留您的帳戶在資料收集執行期間所觀察到的內容。後續的歷史快照無法還原未被記錄的編輯或已刪除的訊息。

**我的整個日誌是否都經過加密？**

帳戶憑證與簽名密鑰均儲存於加密金庫中。本機訊息與附件需存放於加密磁碟或磁碟區。匯出檔案可選擇使用受密碼保護的 AES-256 ZIP 檔案。

**這與 Telegram 有任何關聯嗎？**

不。TgWitness 是一個獨立專案，採用 Telethon 開發，並依據 MIT 授權條款發佈。您可透過內建的 API 設定或您自己的 API 對來授權您的帳戶。

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## 先探索功能，準備就緒後再進行設定。

[開啟示範版](https://phishdestroy.github.io/TgWitness/demo/?lang=zh-Hant)[設定指南](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh-Hant)
