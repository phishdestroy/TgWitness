# 面板指南

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/

面板中的每個畫面：聊天、日誌、來源、匯出、額外功能、保護模式以及程式碼檢查。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [開始使用](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/quickstart/)

![開始使用](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[首次設定與設定選項](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/settings/) · [帳戶](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/) · [匯出與驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/) · [案例報告](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-reports/)

各畫面功能說明、其寫入簽名日誌的內容，以及詳細 指南的位置。面板每次僅顯示一個工作區：一個 Telegram 帳號及其專屬的 來源、日誌與簽名金鑰。側邊欄頂端的選取器可切換 工作區。網址包含工作區資訊（`?ws=…`）；若網址、 選擇器與已載入的帳號不一致，則所有操作將被封鎖。

請使用[「比較」彙整方法](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)，在即時 觀察、完整歷史紀錄、新帳戶／聊天室匯出檔，以及已儲存紀錄移交之間進行選擇。 「匯出」頁面在下載控制項上方亦包含相同的比較功能。

**本頁內容**

- [導覽指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#find-your-way)
- [從這裡開始](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#start-here)
- [聊天紀錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#chats)
- [期刊](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#journal)
- [來源](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#sources)
- [匯出功能](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#exports)
- [設定、帳戶與連線](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#settings-accounts-and-connection)
- [附加內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#extras)
- [保護模式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#protection-modes)
- [更多工具](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#more-tools)

## 探索使用方法

「每日」區塊位於側邊欄頂端，**「帳戶」** 位於「**工作區** 」之下， 其餘項目則位於**「更多工具與設定」** 之下。頂部工具列中的**介面層級** 切換按鈕可決定顯示多少個區塊：

| 層級 | 側邊欄中的區塊 |
| --- | --- |
| 簡單 | 首頁、聊天、變更、存檔和設定 |
| 標準 | 另見 Case Board、「帳戶」與「存取權限」 |
| 專家 | 此外還有「來源」、「附加功能」、「詢問存檔」、「參數」、「帳戶」、「系統日誌」及「整合功能」 |

基本功能包含「從這裡開始」、「日誌」、「匯出**主頁**」、「**變更**」及「**存檔**」。 「層級」僅用於隱藏區段。隱藏的功能仍會持續運作，且伺服器會 自行檢查每項權限。層級、語言、主題和時區會針對 每位操作者及每個工作區分別儲存；詳見[設定](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/settings/)。

頂部工具列還包含：

- **前往特定區段**（Ctrl+K，或在 Mac 上按 ⌘K）：透過 `#number`。使用方向鍵移動，按 Enter 鍵開啟，按 Esc 鍵關閉。
- **通知**：根據日誌處理的問題與聊天室變更。 **點選「全數標記為已讀」**可清空計數器，而**「通知規則」**則會開啟相關設定。 傳送至 Telegram、Discord 或電子郵件的設定位於 [「進階」→「通知」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#notifications)。
- 此工作區的連線狀態指示器。頂部工具列下的「**收集器狀態」** 會將其細分為 Telegram 連線、事件接收、來源及附件佇列。
- **鎖定**：關閉此瀏覽器中的面板。Collection 仍會在伺服器上持續運作。
- 版本號旁邊的保護模式；請參閱[保護模式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#protection-modes)。

示範工作區包含虛構的訊息，且絕不會連線至 Telegram。 任何可能變更真實工作區的操作，在此均會被拒絕。

## 從這裡開始

選擇一項任務。**「匯出我的帳號」**會下載該帳號目前可讀取的內容。 **「追蹤調查」**會記錄您所選聊天室中的新訊息、觀察到的編輯內容以及刪除通知。 設定卡片顯示三個步驟：連線帳號、 選擇來源、開始監測。目標問題會一直顯示在此頁面，直到您 回答或跳過它為止。若開啟新的工作區，則會直接進入[首次設定](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/settings/)流程。

## 聊天室

已儲存的對話，預設為唯讀模式。

- 可透過名稱或 ID 搜尋清單。**選擇**「新增」或「移除」以管理關注的聊天室。 「**開啟 Telegram 連結」**功能接受使用者名稱或邀請連結，並將預覽儲存至 日誌中。**選擇「加入／開啟並觀察」**會先加入該聊天室，再將其新增至您的來源清單； 開啟機器人則會發送該訊息 `/start`.
- 聊天室標題列會統計訊息數量：**已刪除，文字保留**、**在儲存前已刪除** 以及 **重新檢查後未找到**。聊天室清單和通知採用相同的 定義。已刪除的訊息會顯示為紅色，並保留其儲存的文字；經編輯的訊息 則會保留所有儲存的版本。每則刪除紀錄都會顯示已知資訊：何時被查看、 Telegram 不會報告刪除者身分，或是僅收到刪除通知。
- **「載入歷史紀錄」**功能會將最近的 100、250 或 500 則訊息載入至此視圖及 日誌中。若要載入所有已啟用的來源，請使用[「來源」→「完整歷史紀錄」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#sources)。
- **「匯出聊天紀錄」**功能會將整個可見的聊天歷史記錄下載為經簽名的 `chat.json` 且 `chat.html`檔案。多個已連結的帳戶可共同完成此工作：每個帳戶下載其專屬的 訊息編號範圍並對該部分進行簽署，而啟動 匯出的帳戶則對整個檔案進行簽署。請參閱「[匯出單一聊天室](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md)」。
- **「人員」**清單列出所有在此聊天室中存有訊息的使用者。人員個人資料預設為 關閉狀態，因為這些屬於第三方之個人資料。當某個聊天室的 個人資料功能開啟時，個人資料頁面會顯示姓名與使用者名稱歷史紀錄、Telegram 標記、頭像雜湊值、活動紀錄、 誰回覆了誰、其他被監測的聊天室，以及被提及的錢包、手機號碼、使用者名稱 和連結。 每項事實皆指向其對應的記錄。**匯出個人檔案**會儲存一個經簽名的檔案， 可選擇以密碼保護 ZIP；關閉個人檔案功能將刪除該檔案。請參閱「 [人員個人檔案](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#people-profiles)」。
- **「儲存個人資料」功能現可**記錄聊天室或機器人個人資料的快照：描述、 成員、邀請連結、機器人指令。

### 唯讀權限、發送權限與機密資訊

訊息上方有兩個開關，用以保護帳戶與閱讀者：

- 開啟聊天視窗時，預設為**唯讀模式**。 若要發送訊息或按下機器人 按鈕，請將此功能關閉。每次執行動作時，系統都會詢問**「以 @account 身分發送？」**或**「以 @account 身分按下此機器人按鈕？**」，告知您聊天室成員將看到該動作，且該動作會被記錄在 已簽名的日誌中。**選擇「在此聊天室中 10 分鐘內不再詢問」**可暫時跳過此 提示。在「**案件證據**」目標中，無論是在控制面板或 API 中，發送功能均為關閉狀態。
- **「遮罩機密」**功能可隱藏看似密碼、登入碼、API 金鑰或 雜湊值、機器人代幣、會話字串、私鑰、JWT 或支付卡號 （卡號會透過 Luhn 和校驗）的內容。**點擊「顯示」**將揭露一個值；該揭露紀錄 會被記錄在日誌中。針對此瀏覽器關閉遮罩功能的操作也會被記錄下來。 僅顯示內容會改變：原始記錄及所有匯出檔均保留完整內容。

## 日誌

工作區所簽署的每筆紀錄，依最新至最舊的順序排列。

- **「概覽」**會統計已觀察到的訊息、記錄的編輯、刪除通知以及 選定的來源。
- **事件時間軸**可依事件類型（全部、編輯、刪除、反應、 成員資格、報導範圍）、文字內容及來源進行篩選。可**載入較早的事件**頁面。
- 開啟記錄即可查看其詳細資訊、雜湊值及有效載荷。**「此記錄的連結**」是一個 可開啟相同記錄的網址。此預覽中可能的機密資訊已遭遮蔽； 匯出檔則保留原始內容。
- 日誌採「僅追加」模式：面板中沒有任何功能可編輯或刪除記錄。請透過 「**匯出」→「驗證日誌」**或 `python -m tgwitness.verify`；請參閱「 [匯出與驗證」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/)。

## 來源

此工作區會記錄哪些對話，以及從中保留哪些內容。變更 將套用至未來的活動；已儲存的記錄則維持不變。

**「刷新聊天清單」**功能會讀取該帳號的聊天室與資料夾，但不會下載訊息。

### 範圍

- **此帳戶的記錄內容** ：**已選取的聊天室** （僅限您新增的聊天室）、 **Telegram 資料夾** （該帳號的其中一個資料夾，包含日後新增至該資料夾的 聊天室）或 **完整帳戶** （所有聊天室，以及每當出現新的聊天室、群組、私人聊天室或 機器人時皆會記錄）。**調查模式** 適用於專用帳號：它會記錄 該帳號所見的一切內容、其發送的訊息及按鍵操作，並立即儲存每個新 聊天室的檔案及先前可見的訊息。 [專用帳戶指南](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) 說明了為何絕不能使用您的主帳號。
- **來源類型**將「資料夾」與「整個帳戶」模式的範圍限制於頻道、群組、私人 聊天室及機器人。**自訂動作**則會新增該帳戶自身的訊息、編輯操作及 回覆鍵盤按鍵記錄。
- **當出現新的聊天室或機器人時**：儲存其檔案，並儲存最多達指定數量 的最新可見訊息。

限制：已發布的雲端收集器無法接收「秘密聊天」。獨立的 [「偽秘密」介面及其示範版本，](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/secret-chats/)其文件中已註明 開發狀態與尚未解決的缺陷。 當 TgWitness 未 運行時，系統不會進行任何記錄；重新啟動後，它僅會擷取 Telegram 仍能回傳的資料，而 報告中會顯示此期間的資料缺口。超過聊天清單限制（1,000 個對話，除非在 「參數」中進行變更）的聊天室，將於下次變得活躍時被加入。在 其他應用程式中按下的內嵌機器人按鈕將無法被偵測；但機器人的回覆會被記錄下來。

### 涵蓋的聊天室

可依狀態（**啟用**、**暫停**、**優先級**、**排除**、**未確認 存取權限**、**忽略**）及類型進行篩選，接著對選取項目執行操作：啟用、暫停、標記或移除 優先級、從範圍中排除或刪除。狀態標籤僅顯示當前狀態；操作 則位於各列的選單中，並附有說明其功能的文字。 暫停和排除操作會要求 確認，批次操作亦同。移除來源時會要求輸入其名稱，並刪除其人員 檔案；其儲存的記錄仍會保留在日誌中。

若某來源未顯示在該帳戶的聊天清單中，表示該來源正在**接收更新，但未出現在聊天 清單中，**同時記錄仍持續傳入；否則則**無法確認存取狀態**。「**可用 聊天室」**會新增透過「**新增選取項目**」或**「新增所有符合條件的項目」**選取的聊天室。

### 完整歷史紀錄

將每個已啟用來源的可用歷史記錄載入至「聊天」和「日誌」中。 進度會在重新啟動後保留；附件則依照您的媒體設定處理。請參閱 [來源歷史記錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/history/)。

### 記錄

- **選擇要保留的變更項目**：新訊息、編輯、刪除通知、 可見的反應、加入與離開。預設值會變更表單樣式；「 **儲存記錄設定」**則會套用該設定。重新啟用某個類別並不會恢復 已錯過的事件。
- **在可用的情況下保留媒體**檔案：下載單一檔案大小上限為，可針對 各檔案類型設定 1 至 2,000 MiB，並限制影片長度（以秒為單位；0 表示無限制）。 每次下載嘗試都會記錄結果。
- **重新檢查**：每隔幾分鐘檢查一次優先聊天室，其他聊天室則很少檢查，因此該帳號 能避免觸發 Telegram 的 FloodWait 限制。設定為 0 可關閉該群組。在清單中以星號標記優先聊天室； 每次檢查的聊天室數量以及聊天室之間的暫停時間，皆可在 「參數」中設定。請參閱[收藏集](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/)。

## 匯出功能

**「下載」**用於準備檔案；「**建置報告」**則用於設定報告的呈現方式。

| 什麼 | 適用於 | 指南 |
| --- | --- | --- |
| 帳戶匯出 | 該帳號目前可讀取內容的最新快照 | [帳戶匯出](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/account-export/) |
| 分享副本 | 這是已完成的帳戶匯出功能的精簡衍生版本 | [披露聲明](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| 已簽署 ZIP | 在固定的日誌邊界內，包含日誌、報告、附件及驗證工具 | [匯出與驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/) |
| HTML、PDF、JSON 報告 | 一份密封且可讀取的報告 | [案例報告](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-reports/) |
| JSONL、CSV | 附有簽名的原始記錄；一個公式安全的試算表 | [匯出與驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/) |
| 交接摘要 | 僅包含收件者所需的聊天室、時間段及聯絡人 | [證據](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#investigation-handoff) |
| 聊天記錄匯出 | 一則已簽名的聊天記錄 `chat.json` 以及 `chat.html` | [匯出單一聊天室](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **使用密碼加密上述下載檔案**（12 個字元或以上）會儲存一個 AES-256 ZIP，該檔案可透過 7-Zip 或 WinRAR 開啟。其中的簽名檔案內容未經變更。 密碼不會被儲存。
- **「已準備的匯出檔」**會保留最多 20 個檔案（總容量不超過 2 GiB），加上最新的一個檔案，以便 重複下載，每個檔案均包含其 SHA-256。檔案已準備好並不代表已成功傳送。
- 當瀏覽器拒絕顯示儲存對話方塊時，該面板會改為以一般下載方式處理。
- **您的簽署身分**會顯示金鑰指紋。「**儲存檢查點」**與 「下載**已簽署的執行收據」**可讓您取得記錄，以便存放在收集器之外。 「準備**時間戳記請求」**可在不聯繫任何服務的情況下，建立符合 RFC 3161 標準的請求。

## 設定、帳戶與連線

- **設定**：目標、連線、記錄內容及介面。請參閱 [首次設定與設定說明](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/settings/)。
- **帳戶**：每個工作區皆包含其狀態、來源、事件及附件佇列。 可依「**需處理**」、「**正在收集**」、「**離線或暫停**」或「**未 連線**」進行篩選，暫停或恢復選取項目，批次匯入帳戶檔案並管理 群組。詳見[「帳戶」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/)。
- **帳戶**：登入及此帳戶的連線路徑。可選直接連線、WireGuard 設定檔、您自己的代理伺服器、公開的 MTProto 池或 WARP；準備並檢查路徑， 然後將其套用至此帳戶、某個群組或所有帳戶。請參閱 [「連線」、「代理伺服器」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/)及「[代理伺服器](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md)」。

## 額外功能

可選：只需一個帳戶和來源即可開始收集。只有您 選擇的選項才會開啟其設定，系統不會自動建立任何連結。頂部的「 **保護等級**」卡片會顯示當前的[保護模式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#protection-modes)。

| 卡片 | 新增功能 | 指南 |
| --- | --- | --- |
| 儲存與磁碟空間 | 備份、將較舊的檔案移至您的雲端儲存空間，以及一份無法刪除的證據副本 | [儲存空間](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/storage/) |
| 目標與保護等級 | 針對您的目標及兩個量表的建議設定 | [下方](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#goal-and-protection-level) |
| 通知 | 問題、已修改的訊息及每日摘要；您專屬的控制機器人 | [下方](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#notifications) |
| 證據與備份 | 時間戳記、更多見證者以及加密的異地備份 | [下方](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#evidence-and-backups) |
| 伺服器全年無休運作 | 一個不支援 SSH 的雲端伺服器，可透過控制面板進行建立與刪除 | [高可信度](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#from-the-panel) |
| 獨立見證人 | 經簽署的檢查報告將發佈至您的 Telegram 頻道或 Discord | [見證者](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/) |
| 程式碼檢查 | 將正在執行的程式與 GitHub 上的公開提交進行比對 | [下方](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#code-check) |

### 目標與保護等級

四個問題：

1. **用途為何？可用於**個人記錄、調查，或作為案件的證據。
2. **您打算監測多少內容？**少數聊天室（最多約 50 個）、大量聊天室（最多約 500 個）或整個帳戶。這將把聊天室清單的上限設定為 1,000、3,000 或 20,000。
3. **照片和檔案？**僅限文字、照片及短媒體（照片 20 MB、影片 100 MB），或全部（影片和文件各不超過 1 GB）。若選擇包含完整 帳戶的所有內容，則會保留 4 GiB 的可用磁碟空間。
4. **它將在何處運行？**這台電腦，或是一台始終處於開機狀態的伺服器。

建議清單列出了獨立時間戳記、drand 以及 Telegram 的裝置清單，每項 均附有一行說明其新增內容。時間戳記會每 60、30 或 10 分鐘觸發一次，適用於個人 紀錄、調查或證據；drand 和裝置清單則需要時間戳記。僅需 **套用**這些變更、附件政策以及上述兩個參數。每項 變更皆為一則日誌紀錄，此外 `setup.applied`。通知、站外副本、 伺服器、閘道 DNS、程式碼檢查及見證人皆作為後續步驟提供，並附有 各自的表單。

兩項指標是根據設定值計算得出，而非根據目標值：

| 規模 | 重點 |
| --- | --- |
| 可信度 | 簽名日誌 1、時間戳記 3、drand 1、裝置清單 1、代碼核對結果為 1、見證者輪詢 1、經認證伺服器 2、閘道器 DNS 日誌 1 |
| 可靠性 | 常駐伺服器 3 台、異地備份 3 份、Object Lock 1 個、問題通知 1 則 |

**最高**讀取率為 80% 或以上，50% **為高**，25% **為中等**，低於此**則為基礎**。 目前可靠性是根據問題 4 的答案中「始終線上」的伺服器來計算， 且在檢查任何伺服器之前即已納入考量。

### 通知

通知會透過 Apprise 傳送至 Telegram、Discord、Slack、ntfy、電子郵件、Matrix 以及 100 多種其他服務。選擇一項服務，填寫一至兩個欄位並發送測試訊息，或 直接貼上 Apprise 地址。

- **問題**：磁碟空間幾乎已滿、帳戶已登出，以及收集、複製或時間戳記 相關錯誤。在密封伺服器上，開啟的 SSH 埠或登入行為亦屬問題。
- **變更**：在監測的聊天室中，已刪除、編輯及遺失的訊息，會彙整為 每次檢查一則通知（除非在「參數」中變更，否則每分鐘檢查一次）。
- **已完成的功能**：歷史紀錄、匯出功能及儲存副本。
- **每日摘要**將於您選擇的時段（以伺服器時間為準）發送。

通知會顯示聊天室名稱及訊息數量。訊息摘要預設為關閉狀態；若 開啟此功能，訊息內容將傳送至本機以外的伺服器。

**您的操作員機器人**是由 @BotFather 建立的專屬機器人，負責回應 `/status` 並 `/stats`，並可選擇性地 `/pause`, `/resume` 以及 `/copy`。僅列出的聊天室及 Telegram 用戶 ID 可使用此機器人；對話內容將保留在工作區內。若已有其他應用程式接收其指令，請使用獨立的 機器人。請參閱 [「通知」](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md)與[「操作員機器人」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/storage/#operator-bot-and-completion-notices)。

### 證據與備份

- **獨立時間戳記會**每隔 5 至 1,440 分鐘，僅將每個已簽署檢查點的 SHA-256 傳送至 RFC 3161 授權機構及 OpenTimestamps 日曆。**Anchor 目前** 正在執行一次運行。請參閱[時間戳記](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/timestamp/)。
- **更多見證者**，每個見證者在被選中前均處於停用狀態：最新的 drand 輪次、Telegram 的 已登入裝置清單（不含 IP 位址），以及 Cloudflare Gateway 針對伺服器 DNS 查詢的日誌。請參閱[可選記錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)。
- **加密備份會**將日誌、檔案、檢查點及聊天記錄匯出至 S3 相容儲存空間（Wasabi、Amazon S3、Backblaze B2、Cloudflare R2、MinIO）。 所有資料都會先在此機器上進行加密。**請下載加密金鑰**並將其 妥善保管：若無此金鑰，備份副本將無法被讀取。在「治理」或「合規」模式下啟用「物件鎖定」功能， 可防止物件在設定的天數內被刪除。請參閱「[異地備份」](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md)。

### 程式碼檢查

檢查已安裝的程式是否與已發布的版本相符。

1. 請輸入 GitHub 儲存庫（官方儲存庫已預先填入）以及標籤、分支或提交。
2. **「Check now**」會透過此工作區的外部請求路由，向 GitHub API 查詢 該提交的檔案清單。它會將每個被測程式檔案的 Git blob ID 與該提交進行比對。即使是在 Windows 環境下，即使換行符已轉換，仍能匹配成功。
3. 結果清單會列出已變更、新增及遺漏的檔案（每類最多 50 項），並儲存為 一份 `source.checked` 日誌記錄。

結果僅在執行中的程式檔案未變更時才視為有效： 更新後請重新檢查。無需代幣，且僅支援公開儲存庫； 聊天紀錄與憑證不會被上傳。系統透過比對來識別磁碟上的程式碼。這並非 硬體驗證；若需此功能，請參閱 [Phala Cloud](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)。

## 保護模式

版本號旁的切換器會顯示所選模式，以及 18 層 保護層中有多少層處於啟用狀態，例如 `🟠 Witnessed 9/18`。**若要變更模式**，請前往 **「進階」→「保護等級」**以開啟選項。每種模式皆會描述一個目標，並列出 尚待完成的項目；無論哪種模式，記錄、簽名及儲存的設定均保持一致。

| 模式 | 適用於 | 新增功能 |
| --- | --- | --- |
| 🟢 簡單 | 監看聊天室並保留副本 | 「Chats」包含日誌與聊天記錄的匯出功能；簽名作業在背景中執行 |
| 🟡 已簽署 | 向平台、主機或濫用處理部門提交報告 | 簽名存檔、日誌檢查、檢查點、交接摘要 |
| 🟠 已見證 | 可能有人聲稱紀錄遭篡改的情況 | 一個獨立見證者發布經簽署的日誌標題 |
| 🔴 符合法庭採用標準 | 供律師、警方或法院使用的證據 | 時間戳記、加密的異地備份、報告中的案件詳情 |
| 🟣 GitHub 驗證 | 任何人皆應能驗證其軟體的記錄 | 程式碼檢查與 GitHub Actions 擷取 |
| ⚫ 摩薩德 | 針對資金雄厚的對手所進行的高風險案件 | 全天候運作的封閉式伺服器、隱藏的 IP 位址，以及全部 18 層防護 |

各層架構：每筆紀錄皆經簽名並串聯；簽名過的執行收據；以 SHA-256 儲存的附件；簽名檢查點；重新檢查；問題警示；唯讀見證者存取權限； 按排程執行的見證者檢查；RFC 3161 時間戳記；OpenTimestamps 證明；經驗證的 最新時間戳記；加密的異地副本；報告中的案件詳情；代碼 比對檢查； Telegram 絕不會看到這台機器的 IP；外部請求透過代理伺服器進行；副本上的 物件鎖定；一個封存且存有服務供應商紀錄的伺服器。若某個層級處於關閉狀態，會顯示 **「設定」**選項，點擊後將開啟其表單。選擇較低的模式時會要求確認，且 不會刪除任何資料。

## 更多工具

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **查詢存檔**：搜尋已儲存的觀察記錄、檢視來源，然後決定 是否將其傳送至 AI 模型。請參閱[存檔分析](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/analysis/)以及 [本地 OCR 與轉錄功能](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/media-analysis/)。
- **參數**：資料收集的限制與頻率、重新檢查、下載、設定檔、 通知及匯出功能。可依名稱搜尋、顯示 **僅顯示已變更的** 的數值，並透過 **還原預設值…** 將預設值儲存為草稿。**儲存參數** 會從下次使用時起套用這些數值， 且每次變更都會產生一則日誌記錄。
- **存取權限**：審查員、分析師和操作員各有獨立的存取憑證，僅限於指定的 工作區、聊天室及權限範圍。詳見[「存取權限」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/)。
- **系統日誌** ：此程序自啟動以來所執行的操作（連線、代理伺服器變更、 登入、登入失敗、設定變更），其中 IP 位址已隱藏。**「跟隨新行」** 功能可讓最新的一行始終顯示在畫面中。訊息僅保留在日誌中。
- **整合功能**：AI 服務供應商、[唯讀 MCP](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/) 連線以及 [經簽名的 webhook](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/webhooks/)。
- **Case Board**：位於證據旁，包含團隊的私人筆記、書籤和片段。請參閱 [Case Board](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/)。
- **GitHub Actions 擷取功能**在「匯出」中：從您的分支擷取一則聊天記錄。請參閱 [密封擷取](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)。
