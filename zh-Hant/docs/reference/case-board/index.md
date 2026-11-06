# 「案件看板」參考說明

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/

書籤、精確標註、操作片段、討論、範圍限定存取，以及「案件看板」所使用的簽名註解歷史紀錄。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [調查](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/)

![調查](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

「案件看板」為調查團隊提供一個可共享的儲存資料工作視圖。您可以將 觀察結果加入書籤、標示特定段落、儲存一系列操作，並與同事進行討論。 卡片會保留其來源參考資訊及經簽署的修訂歷史紀錄。團隊註解會保留在 工作區中，並可與原始的 Telegram 觀察結果明確區分。

[證據模型](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/) · [存取](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/) · [報告](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-reports/)

![綜合調查資訊流](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

**本頁內容**

- [處理個案](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/#work-with-a-case)
- [權限](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/#permissions)
- [儲存的合約](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/#stored-contracts)
- [API 與匯出功能](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/#api-and-exports)
- [運作限制](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/#operating-limits)

## 處理案件

開啟「**調查」→「案件看板」**，並選擇「標準」或「專家」模式。介面語言將隨選定的模式而定。 在日誌記錄或已儲存的聊天訊息旁點擊**「加入案板」**，或將其設為焦點後按下 **B** 鍵。 點擊一次即可將書籤新增至「收件匣」。編輯其標題、標籤和備註，或將其移至 收藏集。修改後的卡片會附加經簽名的修訂版本；刪除時將保留歷史紀錄。

針對首個案件，請選擇一個蒐集集，並加入能回答某個問題的紀錄。使用「註解」 功能檢視詮釋內容，接著使用「**簡報**」功能逐步瀏覽卡片及來源背景。 在「[報告工作室](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-reports/)」中準備 交付成果時，請另行選擇「案件看板」的素材。儲存切片並不會自動設定報告的資料篩選條件。

在已儲存的聊天訊息中選取文字，即可顯示**「標示 → 看板**」選項。選擇顏色並 新增註解。伺服器會核對精確的引文及儲存版本，包括表情符號、從右至左（RTL）文字及 組合符號。介面不會將選取範圍映射至經過遮罩或轉換的文字上。

在單一聊天中按住 Shift 鍵點擊兩筆記錄，即可執行**「切片」功能**；亦可使用**「按時間切片」**，或儲存 日誌中當前的聊天、時間段及事件類型篩選條件。已儲存的切片具有其專屬的 權威性條件：在日誌中開啟該切片時，亦會套用多重聊天、訊息數量限制及參與者 篩選條件。 **「顯示自書籤新增的記錄」**功能可隔離後續新增的內容。變更 Journal 篩選條件將退出該切片。在「人員」中，使用**「切片此人的操作」**會採用記錄中的行為者 ID； 該功能不會假設訊息作者曾編輯、刪除或對訊息做出反應。

「切片」對話方塊會在允許建立前預覽計數。「`all`」涵蓋所有已記錄的類型， 包括快照、編輯、刪除、反應、成員資格／服務更新、自身操作、 按鈕、媒體結果、已恢復訊息及未來事件類型。此選項描述 已儲存的觀察結果。 「未知聊天室」刪除通知屬於獨立的上下文， 僅限擁有整個工作區存取權限的使用者查看，絕不會歸因於所選的任何聊天室。

各「集合」皆有明定之聊天室範圍。若範圍為空，則代表整個工作區。一個集合 不得包含其範圍外的卡片；受聊天室限制的參與者無法閱讀範圍更廣的 集合。「收件匣」是存放未指派卡片的虛擬集合。 搜尋與篩選功能僅涵蓋可見 的卡片；討論串和提及會繼承父卡片的存取權限。已刪除的留言會在 討論區中留下「墓碑」標記。系統不會記錄瀏覽歷史紀錄。

**「簡報」**模式會開啟所選收藏集中的所有卡片，並提供「卡片」、「來源背景」及「團隊 評論」檢視畫面，以及鍵盤上的「上一則/下一則」控制鍵。此模式不提供任何編輯控制功能。一般 動態消息採用分頁顯示；「簡報」模式會以頁面為單位載入清單，並每次僅擷取一張卡片的詳細資訊。

## 權限

所有操作均需具備 `view`、工作區／聊天範圍及 `board.read` 權限。`board.write` 可新增卡片、 留言、移動以及開啟／審查狀態。`board.manage` 允許進行資料集管理、 確認／駁回狀態，以及修改／移除他人卡片。狀態是團隊 的決策，而非加密驗證結果。

存取表單預設值：審閱者 = 讀取；分析師 = 讀取/寫入；操作員 = 讀取/寫入/管理， 此外還包含其現有權限。現有授權不會自動取得新權限。 主要管理員擁有所有權限，並以「**主要管理員」**身分發佈內容。請使用命名授權 進行權限歸屬。提及清單僅列出目前能夠閱讀完整父卡片內容的存取者。

針對聊天室 A 的授權，即使透過猜測其 ID 或提供 錯誤的 `target.chat_id`，亦無法取得 A+B 的卡片或片段。目標元資料是根據伺服器上的簽名事件雜湊值解析而來。 在回覆前，會先過濾收集項目、討論次數、相關卡片及即時通知。 匯出操作需同時具備 `export` 及 `board.read` 權限；若現有匯出者無看板存取權限，則僅能 取得不含團隊筆記的普通證據檔案。SSE 會在每次批次處理前重新檢查當前的授權狀態。

## 儲存的合約

與觀察記錄類似，註解會以事務性方式寫入工作區中一個僅支援追加的 SQLite 資料表。 `annotations.jsonl` 即是從與 `events.jsonl` 相同的讀取快照所產生的精確標準化匯出檔。 不存在第二個相互競爭的註解儲存庫，亦無 `board.activity` 日誌事件。

每行內容必須精確包含：

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

上述簡化範例展示的是封套結構；實際載荷包含其模型 預設值及由伺服器解析的目標欄位。API 請求架構位於 [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json) 目錄下，由 `python tools/build_board_schemas.py` 透過運行時 Pydantic 模型生成。額外的請求欄位將被拒絕。若未提供 ID，則由 伺服器端自動生成。 呼叫方無法提供 作者、時間、快照及簽名。命名授權 ID 遵循 Access 現有的 16 位元組十六進位格式；卡片 ID 則為 32 位元組十六進位。

規範 JSON 格式為 UTF-8，物件鍵值依序排序，標記之間無空白，Unicode 未經轉義， 且不含 NaN 或無窮大值。註解雜湊值為包含 `format: "tgwitness-annotations-v1"` 以及所有七個信封欄位（至 `previous_hash` 為止）之規範物件的 SHA-256 雜湊值。 此格式標籤將其雜湊域與觀察結果區隔開來。 簽名採用 Ed25519 演算法，基於 32 位元組的原始雜湊值。序列從 1 開始。修訂版本保留卡片 ID，並在 ``supersedes`` 欄位中標明前一版 註解雜湊值；其無法變更聊天範圍。移動、狀態變更及刪除均為 獨立的記錄。SQLite 資料表不接受 UPDATE 和 DELETE 指令。

`case-board.json` 包含 `{statement, signature}`。規範陳述由 工作區金鑰簽署，並包含 `format: "tgwitness-case-board-v1"`、`public_key`、`created_at`、 `journal_head`、`meaning` 及 `state`。狀態為確定性重播：`annotations_head`、一個 有序的 `items` 陣列（包含集合、卡片、註解及墳碑），以及 `status_history`。 各項目在各修訂版本間均保留其最後一次註解雜湊值、序列號、作者與時間，以及原始 建立者與建立時間。重播機制會檢查修訂版本、 父項目、集合參照及重複的操作 ID。`manifest.json` 與新的檢查點 亦會綁定 `annotations_head`。應獨立保留檢查點，以偵測資料遭截斷或 使用複製的簽名金鑰進行改寫的情況。

### 文字版本

`range.start` 為以零為起點的 Unicode 碼點偏移量，`length` 為正數的碼點計數， 而 `quote` 必須與目標事件中 `payload.text` 或 `payload.caption` 的精確子字串完全相符。 不套用 NFC/NFKC、大小寫轉換或字元規範化。 Python 字串切片與 JavaScript 的 ``Array.from(text)`` 實作相同的索引機制。標記與 ZWJ 表情符號的組合可能 佔用多個碼點。``range.version`` 是指目標事件的雜湊值，而非當前訊息 版本或 Telegram 的 UTF-16 實體偏移量。後續編輯絕不會自動重新定位標示範圍。

### 切片識別碼與時間

`query` 函式僅接受一個 `chat_id` 或非空的 `chat_ids` 參數，可選的包含起始點 `from`/`to`、 包含訊息 ID 範圍（僅限單一聊天室）、`kinds: "all"` 或精確/前綴通配符類別、 明確的 `actors`、`search`、`hide_system` 及 `include_unscoped`。日誌類別群組將展開為 其確切的謂詞。 搜尋使用日誌的 NFC／不區分大小寫的載荷搜尋，且不會變更 已簽名的來源文字。日期需指定時區，並歸一化為 UTC。 日期會過濾 **observed_at**。Telegram 的 `source_at` 會另行顯示。若刪除操作未 包含來源時間戳記，則不會生成虛構的刪除時間。在時間區間外觀察到的遲發記錄 不會被納入該區間；針對特定訊息 ID 的訊息 ID 區段，可能包含這些訊息 ID 的較晚刪除記錄。

快照（`snapshot`）會鎖定建立時間、日誌序列/雜湊邊界、匹配計數、首/末 序列以及 `result_hash`。後者是按字典順序排序的匹配 事件雜湊值所構成的 UTF-8 規範 JSON 陣列之 SHA-256 雜湊值，若切片為空則包含 `[]`。 它還包含確切的 類型計數，以及一個 24 區間的觀察時間微型資料。一個切片儲存的是查詢，而非重複的來源 記錄。在匯出時，`board/slices/<id>.json` 會列出當前的雜湊值以及新增／移除的序列。 驗證器會先在建立邊界處重建原始結果，然後重建當前結果。 新增的記錄會以變更事實的形式報告。移除原始事件會中斷不可變的 證據鏈；此操作不會被默默接受為從切片中進行的普通移除。

反應快照中的近期參與者清單不完整。探索器會比較同一則聊天/訊息的相鄰快照 （包括切片範圍外的先前快照），並報告**各觀察結果之間的** 總計數差異。若近期參與者缺失，並不表示該反應已被移除。 第一個快照沒有推斷出的較早狀態。參與者的觀察結果仍歸屬於 其被提供的快照，而非某個虛構的動作時間。

## API 與匯出功能

`GET /api/board` 接受 collection/chat/author/label/state/from/to/q/kind/comments、offset/limit 以及 newest/oldest 排序參數。`GET /api/board/card/{id}` 會傳回卡片、來源預覽、對話串、 狀態歷史紀錄及相關卡片。參與者子路徑會傳回符合條件的提及選項。 `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` 會追加一筆記錄。 `POST /api/board/slice-preview` 會計算查詢結果。切片記錄會透過 `GET /api/board/slice/{id}/records` 進行分頁；重新計算時始終使用當前的穩定讀取快照。 即時 `/api/stream` 會發送不含有效載荷的 `board` 通知，此功能與日誌游標獨立運作。

`GET /api/board/export` 會傳回一份經簽署的文件。受聊天室限制的存取權限將收到一份標示清晰的 經簽署的**披露文件**，絕不會包含其他聊天室的註解或完整對話鏈。完整的證據 ZIP 檔案 包含 `annotations.jsonl`、經簽署的 `case-board.json` 以及切片 JSON 附錄。 HTML/PDF/JSON 報告 設定可選擇「無看板」、「不含討論的書籤／片段」，或「附有評論的卡片」。該 區段會明確區分團隊意見與觀察結果。報告資料篩選器亦會限制 可讀取的筆記內容；證據 ZIP 檔中的完整簽名來源檔案則保持完整。

`GET /api/board/slice/{id}/export` 會產生一個經過簽名的 `tgwitness-board-selection-v1` JSON 摘錄； `?format=csv` 會產生一個方便使用的表格，但不包含獨立的簽名。請保留 JSON 和 ZIP 檔案：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

選取檢查會驗證簽名陳述、精確的來源記錄，以及 其在指定邊界處查詢的完整性。證據 ZIP 檔可能較新，但必須包含該 前綴。若目標懸空，系統會明確報告。若原始切片快照不同、註解 遭變更、重播狀態不匹配或來源變更，則檢查將失敗。 未附註解的舊存檔 將保留其現有的驗證行為。

移交預設為**「不包含**」。 明確包含設定會透過已 簡化的記錄顯示專案卡片，省略無法存取／被省略的目標，隱藏來源文字 已被簡化的重點標記，並依照相同的提及／聯絡規則清理團隊文字，同時可選擇性地將 元資料及筆記中已知出現的調查員標籤替換為 R01、R02…等標記。 不會披露原始的 `annotations.jsonl` 檔案。經簽名的 `tgwitness-case-board-handover-v1` 附檔與報告 均包含相同的最小化內容。切片計數僅描述已披露的記錄，原始 快照／查詢行為者詳情則不予披露。 對於最小化處理程式未知的自由文字名稱，仍需 進行審查，此與一般移交程序相同。此衍生版本並不聲稱在遮蔽處理後能保留原始 註解簽名。

## 操作限制

參數包含 10,000 張卡片與 50,000 則留言的軟性限制、最多 5,000 筆記錄的切片頁面，以及媒體預覽控制。達到軟性限制時會發出警告，但不會刪除歷史紀錄。 動態消息頁面 最多顯示 200 張卡片。獨立 JSON 片段摘錄上限為 64 MiB；若需處理較大資料，請縮小查詢範圍或使用 簽名 ZIP 檔案。獨立驗證器將註解重播上限設定為 256 MiB。 Case Board 未啟用亦未實作任何外部評論通知功能。

此功能的自動化驗收流程會使用虛構資料及模擬的 Telegram 傳輸管道來 檢查儲存、存取、渲染及匯出功能。有關證據檢查的範圍，請參閱[驗證範圍](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope) 。
