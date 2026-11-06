# 命令列

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/cli/

可透過腳本和代理程式進行搜尋、讀取上下文、統計活動次數，並匯出已儲存的訊息，具備 --json 輸出格式、穩定的退出代碼，以及範圍限定的唯讀憑證。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![檔案庫整合](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

[唯讀 MCP](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/) · [全文搜尋](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/) · [維基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**預覽。** `tgwitness search`, `context`, `messages`, `stats` 以及 `export` 讀取 已儲存的觀察記錄，供腳本及 AI 代理程式使用。該工具無法向 Telegram 發送任何內容、變更設定或修改簽名日誌。

當 `--json`，標準輸出（stdout）會傳輸精確一個 JSON 文件（`export` 寫入 JSON Lines）。 進度、提示與錯誤訊息將輸出至 stderr。退出代碼保持不變：

| 程式碼 | 含義 |
| --- | --- |
| `0` | 成功，包括空結果 |
| `1` | 失敗：無法存取面板、資料無法讀取、匯出中斷 |
| `2` | 使用錯誤或無效請求：日期格式錯誤、未知選項、搜尋索引未啟用 |
| `3` | 目前無法使用：工作區已在運行的面板中開啟，或面板要求稍後重試（速率限制、超時） |
| `4` | 存取遭拒：代幣遺失、過期或遭撤銷、聊天室超出權限範圍，或該工具不允許執行此操作 |

## 兩種閱讀方式

**透過控制面板（`--url`）。**此指令使用與 MCP 相同的範圍限定存檔 API。請在**「整合」→「MCP」**中建立連線：選擇工作區與聊天室、 工具及有效期限，然後複製一次權杖。此連線為唯讀模式，僅限 於所選的聊天室，每分鐘請求次數上限為 60 次，且可隨時撤銷或 輪替。控制面板的登入權杖及 Telegram 憑證在此處無法使用。

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

遠端控制面板需使用 HTTPS；僅在以下情況下接受明文 HTTP： `127.0.0.1`, `localhost` 和 `::1`。代理伺服器環境變數將被忽略，且不接受 重定向，因此令牌僅會傳送至您指定的地址。

**直接從已停止的工作區（`--data-dir`）**讀取**。**以 完全本地存取權限讀取資料目錄，無需憑證。請在資料目錄的副本上使用，或於 資料收集停止時使用。簽名記錄絕不會被更改；如同控制面板，開啟 工作區可能會將其衍生的索引更新至最新狀態。當控制面板已開啟該工作區時，此指令會以 代碼 `3`；請改透過面板進行讀取。若未指定 `--data-dir`, `TGWITNESS_DATA`, `./data/live` ，則會使用執行該指令之安裝環境的資料目錄。

`--workspace ID` 選取工作區（預設 `default`). `tgwitness messages
--workspaces` 列出您有權限閱讀的工作區。

## 指令

| 指令 | 結果 |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | 優先顯示最符合的結果，包含詞形變化、加引號的完整短語、網域及 `@username` ([語法](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | 精確文字，最新內容優先，不包含索引 |
| `tgwitness context CHAT_ID MESSAGE_ID` | 前後各十則訊息 ID 範圍內的已儲存訊息 |
| `tgwitness messages` | 可供閱讀的聊天紀錄 |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | 聊天室中已儲存的訊息，最新訊息排在最前 |
| `tgwitness messages CHAT_ID --message ID` | 每則訊息的所有儲存版本及刪除紀錄 |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | 活動統計資料如下 |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | 將觀察記錄以 JSON Lines 格式依日誌順序儲存 |

日期格式為 `2026-10-01` （UTC 午夜）或附有時區的 ISO 時間格式， `2026-10-01T09:00+03:00`。關於 `search`, `messages` 及 `export` ，它們代表 觀察時間。每個頁面最多可容納 50 筆記錄：請遵循 `next_offset` (`--offset`) 進行 排序搜尋，並 `next_before` (`--before`) 其他功能。

排序搜尋結果上限為 1,000 筆。最後一頁的結果數量可能少於 `--limit`；若存在更多符合條件的觀察結果，請縮小查詢範圍、聊天室或時間範圍。

每則訊息結果皆包含 `untrusted_content: true`工作區、聊天室及 訊息 ID、日誌序號、儲存紀錄的雜湊值，以及一個面板連結。編輯、 刪除通知與 `missing_on_recheck` 均為獨立的記錄。若某項記錄缺失 ，並不代表該事件從未發生。

### 活動統計

`stats` 統計特定聊天室、特定發送者或範圍內所有聊天室中已儲存的觀察記錄數量：

- 按 UTC 小時及星期幾（以星期一為起點）分類的訊息；最繁忙的小時與日子；
- 已編輯、刪除及 `missing_on_recheck` 分享；
- 發訊者及其訊息數量，以及第一則與最後一則訊息的時間；
- 最常出現的網域以及 `@handles`，在所有 儲存的版本中，每則訊息僅計數一次；
- 涵蓋範圍： `coverage.gap` 記錄，以及（若要存取整個工作區） 未接收到收集器心跳訊號的期間（`collector_liveness`).

該時間段選取自**Telegram 回報的訊息時間**。小時數與星期數可 協助估算發訊者的時區；但無法據此確定時區。相關數據是根據 請求從日誌中計算得出，並不會儲存。若您的存取範圍涵蓋整個工作區，每個結果會標示其 所涵蓋的日誌起始點。透過 控制面板瀏覽五秒後，或 `--timeout` 本地（預設 30 秒）後，讀取即停止；此時 `complete` 的值為 false，且 `partial` 會標示出第一筆尚未讀取的記錄。在此情況下，僅會 計算最新記錄的數量。

### 匯出

`export` 每筆儲存的觀察記錄（新訊息、快照、 編輯、復原訊息、刪除通知、 `missing_on_recheck` 及已儲存的媒體 記錄），並依日誌順序排列。每行皆包含與其他結果相同的欄位，並附有 完整內容。若 `--output`，檔案將以 `.partial` 名稱下寫入， 並僅在面板完成記錄後才重新命名；若匯出過程中被中斷，則不會產生 檔案，並以代碼 `1`. `--output` 絕不會覆寫現有檔案。若使用 `--output` 和 `--json`，標準輸出將顯示摘要：記錄數、最後的日誌 序列，以及（若為整個工作區存取）日誌頭。

透過控制面板進行匯出時，需具備允許**「匯出訊息」 （僅限命令列）**的連線；此選項預設為未勾選狀態。此檔案僅為工作副本，並非證據：若需可驗證的 移交，請使用「**匯出」**區段中的簽名匯出檔，該檔 `python -m tgwitness.verify`會進行驗證。

該面板在輸出每筆記錄（包括完成 記錄）之前，會重新檢查存取權限。若存取權限已被撤銷或過期，將導致匯出不完整。延遲頁面讀取 會與其他查詢共享存檔工作程序的限制，且設有等待時間上限。

## 代理技能

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) 說明代理程式如何使用這些指令、如何引用記錄，以及如何處理 擷取的文字。讀取 `.agents/skills` 需從儲存庫 的檢出版本中載入該檔案。若使用 Claude Code，請複製 `tgwitness-cli` 資料夾複製到 `.claude/skills/` 您的專案中，或 `~/.claude/skills/`.

## MCP 與命令列介面

兩者均採用相同的連線方式、範圍檢查及限制。MCP 的結果限制為 一個 64 KiB 的頁面，因此 MCP 不提供批量匯出功能；其透過命令列進行串流輸出。 `get_activity_stats` 兩者皆可使用此功能。
