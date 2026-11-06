# 全文搜尋

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/

可透過詞形、精確短語、網域及 @用戶名 搜尋已儲存的訊息，結果依最符合的順序排列，且索引與簽名日誌綁定。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [調查](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/)

![調查](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[檔案分析](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/analysis/) · [本地 OCR 與文字轉錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/media-analysis/) · [維基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**預覽。**在「**日誌**」中，於搜尋欄旁選擇「**最佳匹配 · 詞形變體**」。 搜尋結果依 BM25 演算法排序，並會匹配同一詞彙的其他詞形： *搜尋「перевод」*會找到*「переводом」*和*「переводы」*，搜尋*「transfer」*會找到*「transfers」*，而中文 短語則會以不帶空格的形式被檢索。選擇**「最新優先 · 精確文字」**可維持先前 針對整個記錄進行的子字串搜尋。

索引屬衍生資料。它由簽名日誌重建而成，本身從未經過簽名， 也絕不會被導出。原始記錄不會被更改。

**本頁內容**

- [搜尋語法](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#search-syntax)
- [語言](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#languages)
- [索引的位置](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#where-the-index-lives)
- [結果與已簽署的日誌](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#results-and-the-signed-journal)
- [已識別的文字](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#recognized-text)
- [存取](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#access)
- [請諮詢檔案庫與 MCP](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#ask-the-archive-and-mcp)
- [依賴項](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#dependencies)
- [基準測試](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#benchmark)

## 搜尋語法

| 撰寫 | 搜尋結果 |
| --- | --- |
| `перевод карта` | 同時包含這兩個詞彙的記錄，形式不限 |
| `"переводом на карту"` | 請按此順序保留確切的詞句 |
| `бонус OR подарок` | 任一詞彙 |
| `перевод -казино` | 不含排除詞的記錄 |
| `example.com` | 該網域及其子網域，包括隱藏連結和按鈕網址在內 |
| `@username`, `t.me/username` | 該帳號的提及與連結，以及其發送的訊息 |
| `#tag` | 主題標籤 |
| `+79991234567`、一個錢包地址、一個電子郵件地址 | 以文字或連結形式呈現相同內容 |
| `from:@username`, `from:123456` | 來自該發送者的訊息 |
| `chat:-1001234567890` | 一個聊天室；它只能限制您自身的存取權限 |
| `id:42` | 訊息 42 的儲存版本 |
| `since:2026-01-01 until:2026-01-31` | 觀察期間；未標示時間的日期代表整日 |
| `kind:edited` | 僅限編輯 (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | 以識別出的文字取代訊息，或與訊息並存 |

當存在其他單字時，介詞及其他功能詞將被忽略。 混入單字中的相似字母（例如西文字母「*a」*出現在西里爾字母單字中）、全寬 及裝飾性 Unicode 字母，以及不可見字元，均會被標準化。

## 語言

系統會根據每筆記錄中的腳本和字母來偵測語言：

| 腳本 | 匹配 |
| --- | --- |
| 西里爾字母 | 使用 [pymorphy3](https://github.com/no-plagiarism/pymorphy3) 處理俄語與烏克蘭語詞幹。若未啟用可選的烏克蘭語詞典，則會使用輕量級的烏克蘭語詞幹分析器 |
| 拉丁文 | 英文 Snowball 詞幹提取器；忽略音標符號 |
| 中文、日文、韓文、泰文、老撾文、高棉文、緬甸文 | 重疊字元對：搜尋時不包含空格。中文查詢會使用 jieba 進行分詞 |
| 其他腳本 | 精確詞句 |

烏克蘭語辭典 (`pymorphy3-dicts-uk`) 依據 GPL-3.0 授權發佈，因此 預設不會安裝。請使用 `pip install "tgwitness[uk-dictionary]"`； 索引模組會偵測到新的分析器並自動重新建構。

## 索引的存放位置

| 模式 | 儲存 | 使用說明 |
| --- | --- | --- |
| 儲存於磁碟（預設） | `search/fulltext.sqlite3` 位於工作區目錄中 | 大型存檔；重啟後仍能保留資料 |
| 僅限記憶體中 | 磁碟上不留任何資料；每次啟動時皆重新建置 | 磁碟上不會存有訊息內容的任何衍生副本 |
| 關閉 | 無索引；**最新內容優先 ·** 保留**原始文字** | 最低安裝需求 |

主要管理員可於「**日誌」→「篩選器」→「搜尋索引」**中 為每個工作區選擇模式。 `TGWITNESS_FULLTEXT=disk|memory|off` 並為 未自行設定的空間設定預設值。切換至「記憶體」或「關閉」將刪除該檔案。 索引檔案與日誌享有相同的保護措施：它存放於私有資料 目錄中。該檔案未經加密，且不包含在備份或異地副本之中。

新記錄會在數秒內於後台完成索引；搜尋時也會優先索引 短暫的歷史記錄，因此剛儲存的記錄也能被找到。現有的日誌會在 更新後完成索引，且不會阻塞控制面板；在此之前，搜尋結果涵蓋 已索引的記錄，而日誌會顯示進度。**重建索引時**會從 第一筆記錄開始重新進行。

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` 需停止該面板（否則退場代碼為 3）。若使用 `--json`， 標準輸出僅顯示結果；進度訊息則輸出至標準錯誤。

## 結果與簽名日誌

索引會儲存其所涵蓋之最後一筆日誌記錄的序號與雜湊值， 並在開啟日誌時將其與日誌內容進行比對。若日誌遭替換、還原或編輯， 則會觸發索引重建。每次回應都會回報此位置，而每次查詢結果皆 透過其序號從簽名日誌中讀取：索引僅決定 應顯示哪些記錄及顯示順序，絕不涉及記錄內容。聊天室存取權限僅適用於 日誌本身的聊天室欄位，不適用於索引內容。

## 已識別的文字

OCR 結果與轉錄內容仍保留於其加密的原始檔中。其索引僅存在於 記憶體中，並會在辨識任務完成時重新建置。當出現匹配結果時，該結果會顯示於其 `media.saved` 記錄上會顯示一個匹配結果，標記為「機器識別」，並附有引擎、模型及 摘錄內容；該內容絕不會以 Telegram 傳送的文字形式呈現。同一索引亦供 **「搜尋已識別文字**」功能使用，該功能同時仍可匹配純文字子字串。

## 存取

「聊天室範圍」存取僅會搜尋來自該聊天室的記錄，包括其附件中 被識別的文字。 `chat:` 以及其他篩選條件僅能進一步縮小該資料集範圍。顯示給範圍內存取的索引狀態 會省略日誌總數。僅有主要管理員才能變更 模式或重建索引。

## 請諮詢檔案庫與 MCP

當索引建立完成後，**查詢功能**將從此索引擷取來源： 選定聊天室中的最佳匹配結果，且每則已儲存的文字僅計入一次。最多會傳送 24 個來源；長篇文字會以匹配內容為界截斷，並標記為「截斷」。 關於近期變更、單則訊息的儲存版本，以及在 索引仍在建立期間的搜尋，均使用先前的按時間順序檢索方式。預覽 畫面會顯示所使用的檢索方法。

MCP 客戶端可呼叫 `search_messages` 透過 `ranked=true` ，並透過 `next_offset`。範圍限定連線僅會接收其對應的聊天內容。

排序分頁最多涵蓋前 1,000 筆結果，無論頁面大小為何。請縮小查詢範圍、聊天室或時間範圍，以檢視更多匹配結果。按「最新優先」搜尋時，系統會在選取各頁面之前，先將訊息、OCR 及轉錄結果依此順序排列。

## 依賴項

| 套件 | 授權條款 | 原因 |
| --- | --- | --- |
| pymorphy3、pymorphy3-dicts-ru、DAWG2-Python | MIT | 俄語與烏克蘭語詞幹；詞典於本地載入 |
| snowballstemmer | BSD-3 條款 | 英文詞幹，純 Python |
| jieba | MIT | 中文查詢分詞，純 Python 實作（僅提供原始碼發行版） |
| pymorphy3-dicts-uk（可選） | GPL-3.0 | 完整的烏克蘭語詞典 |

SQLite FTS5 需搭配 `unicode61` 分詞器；此功能已包含於 當前 Python 建置版本的 SQLite 中。若未啟用，最佳匹配搜尋將回報該功能不可用。

## 基準測試

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`建立一個包含俄語、烏克蘭語、英語、 中文及日語訊息的確定性簽名日誌，內容涵蓋 200 個聊天室中的連結與識別碼，並建立索引 以及測量典型搜尋所需時間（50 筆結果，7 次執行中的中位數）。

測試環境：Windows 11、Intel Core i9-13900K、128 GB 記憶體、Python 3.12.10、SQLite 3.49.1，資料儲存於 exFAT 磁碟機，分析器 `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| 度量 | 結果 |
| --- | --- |
| 簽名日誌 | 1,000,000 則訊息，1.50 GiB，於 19 分鐘內寫入 |
| 從日誌建立索引 | 71 秒，約每秒 14,141 則訊息 |
| 索引檔案 | 58 MiB，佔日誌的 3.8% |
| 在新記錄生成後立即進行搜尋 | 中位數 8 毫秒，第 95 百分位數 9 毫秒 |
| 先前子字串搜尋，同一日誌 | `перевод` 3.2 秒， `银行转账` 2.6 秒， `verify-account.example` 2.6 秒 |

| 搜尋 | 匹配的記錄 | 最佳匹配、中位數 | p95 | 最新優先，中位數排序 |
| --- | --- | --- | --- | --- |
| 常見詞彙及其詞形： `перевод` | 134,403 | 82 毫秒 | 85 毫秒 | 7 毫秒 |
| 兩個字： `оплата карта` | 28,996 | 43 毫秒 | 43 毫秒 | 14 毫秒 |
| 生僻詞： `розыгрыш подарок` | 28,881 | 42 毫秒 | 47 毫秒 | 13 毫秒 |
| 精確短語： `"переказ коштів на картку"` | 不計入 | 35 毫秒 | 36 毫秒 | 6 毫秒 |
| 網域及其子網域： `verify-account.example` | 12,435 | 17 毫秒 | 17 毫秒 | 3 毫秒 |
| @使用者名稱： `@support_desk_bot` | 10,331 | 15 毫秒 | 16 毫秒 | 3 毫秒 |
| 中文（無空格）： `银行转账` | 17,691 | 23 毫秒 | 24 毫秒 | 3 毫秒 |
| 日文： `リンク` | 16,603 | 23 毫秒 | 25 毫秒 | 3 毫秒 |
| 英文詞幹： `withdrawal` | 27,775 | 26 毫秒 | 26 毫秒 | 2 毫秒 |
| 或與排除： `бонус OR подарок -казино` | 268,034 | 190 毫秒 | 193 毫秒 | 19 毫秒 |
| 聊天過濾器： `chat:-1000000000007 перевод` | 652 | 9 毫秒 | 9 毫秒 | 6 毫秒 |
| 時間範圍篩選器： `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 毫秒 | 156 毫秒 | 81 毫秒 |

系統會依排名順序，逐一對候選結果進行字面比對，直到頁面 填滿為止，因此其總數不計入統計。搜尋時間會隨匹配記錄的數量增加而增長； 縮小聊天室範圍或時間區間，可加快廣泛搜尋的速度。合成語料庫重複 使用少量詞彙，因此常見詞彙所匹配的記錄數量遠多於真實聊天記錄。
