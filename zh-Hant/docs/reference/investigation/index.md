# 調查模式

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/

涵蓋頻道、群組、私人聊天及機器人的完整帳戶調查，從調查範圍到經核實的案件檔案包。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

可跨頻道、群組、私人聊天室及機器人追蹤案件，從最初的 資料擷取，到帶有引用時間軸及可驗證的交接流程。互動式網站 版本位於 `/docs/cases/`；[預覽說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally)。

**On this page**

- [Worked case: a destination changes across four conversations](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/#worked-case-a-destination-changes-across-four-conversations)
- [1. Define the case and collect the whole account](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/#1-define-the-case-and-collect-the-whole-account)
- [2. Inventory every source and acquire historical context](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/#2-inventory-every-source-and-acquire-historical-context)
- [3. Preserve the evolving case and deliberate interactions](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/#3-preserve-the-evolving-case-and-deliberate-interactions)
- [4. Connect observations across chats](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/#4-connect-observations-across-chats)
- [5. Build the cross-chat timeline](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/#5-build-the-cross-chat-timeline)
- [6. Add account perspectives without losing their origin](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/#6-add-account-perspectives-without-losing-their-origin)
- [7. Assemble and verify the case handoff](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/#7-assemble-and-verify-the-case-handoff)
- [Adapt the investigation](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/#adapt-the-investigation)

## 案例分析：四段對話中目的地資訊的變更

一則公告指向一個聊天機器人。一個行動小組討論新的付款 目的地，而該聊天機器人的鍵盤上顯示了該目的地。該公告經過編輯， 一則私訊跟進時重複了該目的地，而一則群組訊息則消失了。

問題包括：變更前後觀察到什麼情況、哪些 Telegram 帳號發布了各項內容、目的地出現在何處、哪些附件位元組 被保留下來，以及哪些時間間隔仍屬未知？

本範例中的所有名稱、ID、時間及日誌參考資料均為虛構。該 工作流程採用現行功能；案例地圖僅為示意圖，並非由應用程式自動 生成的圖表。

流程圖 · 頻道 → 工作區日誌; 群組 → 工作區日誌; 私人聊天室 → 工作區日誌; 機器人 → 工作區日誌; 工作區日誌 → 搜尋所有來源; 工作區日誌 → 附有記錄參考資料的人物檔案; 工作區日誌 → 已儲存版本與附件收據; 搜尋所有來源 → 分析師時間軸與來源登記簿; 附有記錄參考資料的人物檔案 → 分析師時間軸與來源登記簿; 已儲存版本與附件收據 → 分析師時間軸與來源登記簿; 工作區日誌 → 經簽署的證據 ZIP 檔案; 分析師時間軸與來源登記簿 → 附有經獨立驗證之證據資料的案件移交; 經簽署的證據 ZIP 檔案 → 附有經獨立驗證之證據資料的案件移交 · 頻道 · 群組 · 私人聊天室 · 機器人 · 工作區日誌 · 搜尋所有來源 · 附有記錄參考資料的人物檔案 · 已儲存版本與附件收據 · 經簽署的證據 ZIP 檔案 · 分析師時間軸與來源登記簿 · 附有經獨立驗證之證據資料的案件移交

**圖表轉為文字**

1. 頻道 → 工作區日誌
2. 群組 → 工作區日誌
3. 私人聊天室 → 工作區日誌
4. 機器人 → 工作區日誌
5. 工作區日誌 → 搜尋所有來源
6. 工作區日誌 → 附有記錄參考資料的人物檔案
7. 工作區日誌 → 已儲存版本與附件收據
8. 搜尋所有來源 → 分析師時間軸與來源登記簿
9. 附有記錄參考資料的人物檔案 → 分析師時間軸與來源登記簿
10. 已儲存版本與附件收據 → 分析師時間軸與來源登記簿
11. 工作區日誌 → 經簽署的證據 ZIP 檔案
12. 分析師時間軸與來源登記簿 → 附有經獨立驗證之證據資料的案件移交
13. 經簽署的證據 ZIP 檔案 → 附有經獨立驗證之證據資料的案件移交

## 1. 界定案件並完整記錄事件經過

1. 請在專屬的工作區中連結資料蒐集帳戶。在「[案件看板」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/) 或您的案件登記簿中，記錄案件參考編號、帳戶 ID、工作區及 觀察起始時間。請獨立保留可信簽名金鑰的指紋。
2. 若要建立專用的蒐集帳戶，請開啟**「來源」→「觀察範圍」→「調查模式」**。此預設選項會選取「 **整個帳戶**」、頻道／群組／私人聊天／機器人、自身操作、來源 檔案，以及新發現來源的最新 200 則可見訊息。 檢視設定後，按下**「儲存範圍」**，並完成範圍確認。 主要帳戶可使用選定的聊天室或資料夾；全帳戶收集功能 僅限標記為「調查中」的帳戶使用。
3. **載入聊天記錄**，並將來源與該帳號的對話清單進行比對。 檢查 排除項目。**參數 → 從帳號清單中讀取的聊天室數量**預設為 1,000 則，最多可達 20,000。超出清單限制的來源會在 其變得活躍時被加入。記錄實際枚舉的內容。
4. 在「**記錄設定**」中，選取「**所有可見活動**」，並儲存 監控設定。請檢視附件類型／限制及可用磁碟空間。
5. 開始監測。驗證一則受控的新訊息、編輯及刪除操作，接著 保留測試參考資料及任何失敗紀錄。

「整個帳戶」範圍會根據儲存的設定，記錄該帳戶可見的所有活動。 本工具不會存取秘密聊天，也不會自動加入所有連結的群組。此外， 也不會回溯補錄所有現有的對話紀錄。請參閱[「資料蒐集範圍」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account)。

## 2. 清點所有來源並蒐集歷史背景資訊

建立來源登記簿，每則聊天記錄佔一行：

| 領域 | 記錄 |
| --- | --- |
| 品牌定位 | 工作區、帳號 ID、數值聊天室 ID、標題及類型 |
| 能見度 | 會員身分／角色、存取權限已確認或未確認、排除項目 |
| 即時擷取 | 開始時間、選定的事件類型及後續政策變更 |
| 日誌歷史 | 快照請求／完成狀況、限制、時間及記錄參考資訊 |
| 完整歷史紀錄 | 經簽署的每則聊天室匯出檔案名稱、邊界及完成／失敗狀態 |
| 附件 | 已完成的媒體收據、雜湊值、大小以及跳過／失敗的結果 |
| 涵蓋範圍 | 服務中斷、資料擷取不完整、FloodWait、無法取得訊息及其他資料缺口 |

針對每個來源，請選用適當的擷取方式：

- 「在**來源**中**載入完整歷史紀錄」**會將已啟用的來源中可用的過往 訊息載入至工作區日誌。此功能支援暫停／恢復 ，並提供經簽名的進度報告。請參閱[歷史紀錄擷取](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/history/)。
- **歷史快照**會將近期可見的訊息儲存至觀察日誌中。 預設上限為 500 則；透過「**參數 → 最大歷史快照」**可將 此上限提高至 10,000 則。這些是當前的歷史觀察記錄，而非重建的編輯紀錄。
- **「完整聊天記錄匯出」→「匯出完整聊天記錄**」，或「**聊天」→「匯出聊天記錄**」，會將 某個聊天室當前可見的歷史紀錄匯出至獨立的、經簽名的 `chat.json` / `chat.html` 封裝檔中。請針對案件中的各來源重複此步驟，並保留每個結果。
- **當出現新的聊天室或機器人時，**可儲存其檔案及多達 1,000 則近期 訊息；若啟用「調查模式」，則僅選取 200 則。當啟用該模式時，現有聊天室不會 追溯性地接收這些資料。
- **下載可見附件**時，會根據設定的政策保留對應的位元組數。 必須具備包含 SHA-256 雜湊值及位元組數的完整 `media.saved` 收據。排入佇列的 工作、縮圖或檔案名稱均不屬於被保留的附件。

完整聊天記錄匯出並不會將所有 訊息填入日誌或人員檔案中。若需在 TgWitness 內分析特定歷史紀錄，請使用**「載入完整歷史紀錄」**或「有限範圍的日誌快照」。在開始 執行歷史紀錄處理前，請先檢視已啟用的來源清單。無論採用何種方式，均無法恢復 Telegram 已不再回傳的內容。

## 3. 保存不斷演變的案件及有預謀的互動

將活躍案件的聊天室標記為優先來源。檢視重新檢查間隔、持續 的補錄進度及媒體結果。使用該帳號時，請保持收集器處於監測狀態。 請使用**「聊天室」→「個人檔案」→「立即儲存個人檔案」**，以保留來源元資料，例如 描述和機器人指令。此功能與從已儲存訊息衍生出的 人員個人檔案是分開的。

當案件涉及追蹤消息來源或與機器人互動時：

1. **開啟 Telegram 連結 → 儲存預覽：此功能**會在執行操作前，將提供的連結及其 預覽內容記錄下來。
2. **「加入／開啟並觀察」**會執行加入／開啟操作，並在提供時傳送機器人的 start 參數。待審核的加入請求將被記錄為「待處理」。
3. 面板發出的文字回覆及受支援的按鈕點擊操作將保留 `interaction.requested` 和 `interaction.result`。回調收據可保留 返回的彈出視窗文字、警示狀態及 URL。

這些是真實的帳戶操作。在另一款 Telegram 應用程式中按下的回調按鈕， 收集器無法偵測到，儘管由此產生的訊息或編輯操作可能會被記錄。 此迷你客戶端不執行網頁應用程式、支付、電話或位置相關的工作流程。 有關確切的運作行為，請參閱[面板互動說明](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/#act-from-the-panel)。

## 4. 串聯不同聊天室中的觀察結果

在「**日誌**」中，選取「**所有來源」**並搜尋已記錄的內容。開啟符合條件的 記錄，並保留工作區、聊天室、訊息 ID、序列號及記錄雜湊值。

在相關聊天室中，開啟「**人員」→「開啟個人檔案」**，並檢視某位使用者：

- 隨時間推移所觀察到的名稱／使用者名稱，以及 Telegram 的數值 ID。
- 回覆內容需包含原始記錄的引用資訊。
- **另見……**此工作區日誌中該 ID 曾發言的其他聊天室。
- 活動紀錄、編輯／刪除紀錄，以及被提及的錢包、手機、使用者名稱和連結。
- 已儲存的頭像元資料及類似的快取頭像，並標示其各自的來源。

在調查結果中使用衍生個人檔案前，請先開啟所引用的紀錄。個人檔案涵蓋 擁有儲存訊息的對象，而非群組中的每位成員。**「參數」→「每項事實引用的紀錄數」** 僅會限制參考清單的範圍，而非底層活動的計數。 提及內容與頭像相似度僅為線索；它們並不能確立所有權或身分。

在示例中：

| 連結 | 記錄 | 受支援的觀察項目 |
| --- | --- | --- |
| 同一發送者帳號 | 群組 #146 及後續私訊 #205 | 兩者均提供 Telegram 發送者 ID 71001 |
| 相同目標 | #146、機器人鍵盤 #173、頻道編輯 #188、私訊 #205 | 所有內容均包含`pay.example.invalid/new`；所有權／控制權尚未確立 |
| 相同的儲存檔案 | 已完成媒體收據 #151 和 #209 | 所保存位元的完整 SHA-256 值完全一致 |
| 頻道來源標示 | #101 和 #188 | 若未標明發送者，請勿將頻道貼文歸因於使用者 71001 |

Compare attachment hashes and their associated message references, and keep account timelines grouped by the Telegram IDs supplied in those records.

請將團隊的工作筆記保留在[「案件看板」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/)上：將您依賴的紀錄 （例如 #146、#188 和 #205）加入書籤，標示出確切的目標字串，並 儲存兩個紀錄之間或特定時間範圍內每項記錄動作的片段。 筆記 與狀態會將團隊的審閱內容保留在其各自的簽名歷史紀錄中，可與 原始觀察結果分開識別。

## 5. 建立跨聊天室的時間軸

請使用**「聊天室」**中的儲存版本及其「**日誌記錄 #…」**連結。在 **「日誌**」中，將**所有來源**與**編輯**、**刪除及涵蓋範圍**合併。 若已提供，請同時保留 `source_at` 與 `observed_at`。

| 示意性觀察時間 | 參考資料 | 觀察 |
| --- | --- | --- |
| 09:00 | 頻道 #101 | 原始目的地已記錄 |
| 09:12 | 群組 #146；媒體 #151 | 已發布新目標；檔案下載完成 |
| 09:16 | 機器人 #173 | 鍵盤指向新的目的地 |
| 09:20 | 頻道 #188 | 公告已編輯；兩個儲存版本均保留 |
| 09:24 | 私密 #205; 媒體 #209 | 同一發送者 ID 的收件者重複；原始檔案位元組內容完整保留 |
| 09:28 | 群組 #231 | 已收到刪除通知；刪除者及確切刪除時間不詳 |

其他記錄可能出現在這些範例參考資料之間。序列號用於排序 觀察結果；歷史快照可能包含較早的來源日期，且傳送時間可能晚於 即時事件。請區分快照、已恢復訊息、刪除通知以及 重新檢查時發現缺失的結果。 請將覆蓋範圍的缺口標記為「未知區間」。後續 取得的历史資料，並不能追溯性地確立觀察過程的連續性。

## 6. 新增帳戶視角，同時保留其原始來源

針對每個獨立帳戶使用獨立的工作區，並重複執行其清點程序。 每次比對時，請保留帳戶 ID、角色、簽名金鑰指紋及來源參考資訊。 訊息編號並非適用於所有聊天室／帳戶的通用識別碼。

「案件看板」會在每個工作區內保存與來源連結的筆記和彙整資料。 群組畫面可共同檢視帳戶狀態，並能整合來自不同工作區的 匯出檔案。您可在案件筆記或分析工具中將這些來源相互關聯；每個日誌 皆保留其原始來源與簽署金鑰。系統不會產生全域搜尋或合併跨工作區 的時間軸。 單一頻道／超級群組的多帳戶匯出 會透過符合資格的帳戶取得該聊天室的歷史紀錄。

針對較長期的作業，應透過[獨立見證人](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/)維持界線。 使用受控傳送檢查來驗證 每個帳戶的擷取路徑與可見性。

## 7. 彙整並驗證案件移交

請將以下資料彙整於由分析師編製的案件檔案夾中：

| 資料 | 目的 |
| --- | --- |
| 案件筆記與來源登記簿 | 問題、資料蒐集政策、存取權限／角色、調查結果、替代解釋及資料缺口 |
| 時間軸 | 每則記錄均包含時間資訊，以及工作區／聊天室／訊息／序列的相關參考資料 |
| Case Board 若已使用，則包含匯出與片段 | 與來源連結的書籤、引文、團隊筆記、彙整集、修訂歷史紀錄，以及經與證據 ZIP 檔案比對後選定的紀錄 |
| 每個工作區的簽名證據 ZIP 檔案 | 完整的記錄日誌、清單及所包含的保存媒體；面板篩選器不會縮小日誌的匯出範圍 |
| 獨立簽署的用戶檔案 | 已將衍生參考資料與對應的工作區證據進行比對核實 |
| 經簽署的完整聊天記錄匯出檔 | 當前可見歷史紀錄的擷取功能，與觀察日誌分開處理 |
| 可信指紋與早期檢查點 | 關鍵身分識別與保留日誌的範圍界定 |
| 若已進行設定，則會產生 Witness 證據檔案 | 獨立日誌、經簽署的貼文及證據指紋 |
| 驗證結果與傳送檔案的雜湊值 | 已核實的內容、傳輸的位元組以及傳輸對象 |

來自可信賴的安裝來源，包含檔案名稱及各工作區的實際指紋：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

請保留實際的驗證結果及原始證據資料。將「案件看板」中的工作區 筆記與引用的來源資料一併匯出。將跨工作區 的調查結果彙整至頂層案件目錄中；每個 TgWitness 證據資料皆擁有專屬的 簽章及驗證程序。

## 調整調查方式

| 案例 | 追蹤 | 交付 |
| --- | --- | --- |
| 由機器人驅動的訂單／付款爭議 | 條目公告 → 已儲存連結預覽 → 機器人啟動參數 → 訊息與鍵盤版本 → 面板回呼收據 → 私人／群組後續追蹤 | 已觀察到的提議／回應時間軸及經核實的來源；僅憑付款連結並不能證明已付款 |
| 事件發生後被刪除的訊息 | 所有受影響的聊天室 → 已儲存的原始內容／編輯紀錄 → 刪除或重新檢查時內容缺失的結果 → 已保存的媒體檔案 → 事件涵蓋範圍及其他帳戶視角 | 保留原始版本並明確標示未知時間區間；不假設任何虛構的刪除行為者 |
| 某位參與者在不同聊天室中使用不同的名稱 | Numeric sender ID → name/username history → replies → other observed chats → cited destinations/files | Telegram 帳號的活動時間軸，附有其來源記錄的連結 |

[資料彙編參考](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/) · [個人資料驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#people-profiles) · [證據移交](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#investigation-handoff) · [驗證已完成](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/)
