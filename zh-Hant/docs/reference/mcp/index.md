# 唯讀 MCP

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/

將 MCP 客戶端連接到選定的工作區和聊天室，並賦予其具有有效期限且可撤銷的存取權限。

將分析師用戶端連線至選定的工作區與聊天室。TgWitness **在面板行程中的 `/mcp` 提供 Streamable HTTP 服務**。每個連線都有獨立的權杖、到期時間與授權工具。MCP 無法傳送 Telegram 訊息、變更設定或修改已簽章的日誌。

[工作流程指南](https://phishdestroy.github.io/TgWitness/docs/archive/) · [維基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## 安裝與檢查

請使用執行面板的 Python 環境。從原始碼檢出目錄執行：

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

安裝完成後，請使用慣用的資料目錄與啟動引數重新啟動面板。就緒狀態應包含 `[PASS] mcp: streamable-http available`。 **Integrations → MCP** 會顯示執行階段狀態，以及使用該伺服器實際 Python 執行檔的安裝指令。**Re-check** 會在不重新載入頁面的情況下重新整理此狀態；它不會安裝套件或重新啟動伺服器。

此 MCP 擴充套件使用官方的[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)。`deploy/constraints-mcp.txt` 固定了經過測試的 SDK 及其依賴項。

## 核發連線

1. 輸入標籤，並選擇允許用戶端讀取的工作區與聊天室。
2. 逐一選擇工具或使用預設組合。系統僅提供已實作的工具。
3. 選擇 1、7、30 或 90 天，或設定介於 1 分鐘至 90 天之間的自訂到期時間。
4. 按下 **Create connection**。權杖會在用戶端設定旁顯示一次。
5. 複製權杖與設定，接著執行 **Check connection**。這會初始化 MCP 並列出授權的工具；**不會讀取任何訊息**。結果會顯示通訊協定版本、工具名稱、數量與耗時。
6. 儲存憑證後按下 **Done**。輪詢期間會保留表單與僅顯示一次的卡片。鎖定面板會清除畫面上顯示的機密資訊。

清單會顯示近期使用情況、最後使用的工具、位址以及過去一分鐘內的請求數。 **Revoke** 會終止存取權限。**Rotate token** 會撤銷舊憑證，並核發具有相同範圍、工具與到期時間的替代權杖；請單次複製該替代權杖。 面板登入權杖與 Telegram 憑證無法作為 MCP 權杖使用。

## 連接您的用戶端

在面板中選擇用戶端並複製產生的設定。設定檔會使用機密參照或明確的預留位置；權杖需另外複製。

| 用戶端 | 設定 | 連結 |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP、`type: "http"`、Bearer 標頭 |
| Claude Desktop | `claude_desktop_config.json` | 本機 stdio 橋接器 |
| Cursor | `.cursor/mcp.json` | 使用環境變數標頭的 HTTP |
| VS Code Local | `.vscode/mcp.json` | 使用密碼 `promptString` 輸入的 HTTP |
| Windsurf | `mcp_config.json` | 使用 Bearer 標頭預留位置的 HTTP |
| 其他用戶端 | URL 與 Authorization 標頭 | Streamable HTTP |

TgWitness 使用 Bearer 權杖，不支援 OAuth 自動探索。若用戶端的遠端連接器要求使用 OAuth，請改用本機 stdio 橋接器。針對 VS Code，輸入變數僅適用於 **Local** 執行環境，不會轉發至 Copilot 工作階段。 設定參考文件：[Claude Code](https://code.claude.com/docs/en/mcp)、[Cursor](https://prod.cursor.com/docs/mcp)、[VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)。

本機橋接器的標準進入點為：

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

請使用用戶端本機已安裝 MCP 擴充套件的 Python 環境。在其受保護的環境中設定 `TGWITNESS_MCP_TOKEN`。請勿將憑證寫入指令引數與 URL 中。`tgwitness-mcp` 是相同的進入點。舊的 `tgwitness.mcp_bridge` 模組與 `TGWITNESS_ARCHIVE_TOKEN` 名稱仍作為相容性路徑保留並會發出警告；新的設定請使用 `mcp_server` 與 `TGWITNESS_MCP_TOKEN`。

## Cloudflare Tunnel

轉發面板的 `/mcp` 路由並保留 Bearer 標頭。以管理員身分開啟 MCP 設定時，會為當次執行註冊面板目前的來源位址（Origin）。 若要在重新啟動後立即擁有穩定的可用位址，請在啟動面板前，將面板的 HTTPS 來源位址設定至 `TGWITNESS_PUBLIC_URL`。 任意的 Host 與轉發標頭不會註冊為受信任的位址。 Host 與 Origin 檢查會拒絕不相關的瀏覽器來源。回應會使用 `Cache-Control: no-store`；授權值絕不會被記錄至日誌中。

`*.trycloudflare.com` 位址是暫時性的。當通道重新啟動並變更主機名稱時，請更新已設定的公開 URL 以及各個用戶端的 MCP URL。針對需要儲存的用戶端設定，請使用穩定的主機名稱。

## 工具與權限邊界

| 工具 | 讀取內容 |
| --- | --- |
| `list_workspaces` | 已授權的工作區 |
| `list_chats` | 已授權的聊天室 |
| `search_messages` | 指定期間內已儲存的訊息文字 |
| `get_message_versions` | 已擷取的版本與刪除觀測記錄 |
| `get_message_context` | 鄰近的已擷取訊息 ID |
| `get_journal_event` | 單筆經過清理的記錄及其來源參照 |
| `get_capture_status` | 收集狀態與授權的涵蓋範圍記錄 |

`tools/list` 僅會回傳授予該連線的工具。對其他工具的呼叫將會被拒絕。此組建不提供群組脈絡、事件片段（episode）、術語及回覆鏈工具；系統未包含這些工具獨立的 context-pack 後端。

每次讀取都會檢查權杖、工具以及工作區／聊天室範圍，包含在資料庫作業完成之後的檢查。限制為每分鐘 60 次請求、每頁 50 筆記錄、每筆結果 64 KiB，以及 8 秒的封存查詢時限。逾時的 MCP 呼叫會回傳工具錯誤，要求縮小時間範圍或降低筆數上限。

訊息結果包含 `untrusted_content: true`、工作區／聊天室／訊息 ID、事件序號、已儲存的雜湊值以及面板連結。原始 Telegram 物件、存取雜湊（access hashes）、工作階段與金鑰均會被省略。文字截斷處會加以標記。編輯、刪除通知與 `missing_on_recheck` 為各自獨立的觀測結果。缺少記錄並不能證明某個事件從未發生。

請將擷取訊息內的指示視為證據，切勿將其作為用戶端指令執行。唯讀存取權限可防止封存內容遭竄改；但用戶端仍可保留其獲准讀取的內容。雜湊值用於識別已儲存的記錄並支援完整性檢查；它們無法證明 Telegram 的作者身分或擷取內容的完整性。
