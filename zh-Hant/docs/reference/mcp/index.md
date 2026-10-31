# 唯讀 MCP

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/

將 MCP 客戶端連接到選定的工作區和聊天室，並賦予其具有有效期限且可撤銷的存取權限。

**當前主要版本：**請使用原始碼檢出；0.7.0 便攜版預覽版尚未包含此功能。

[工作流程指南](https://phishdestroy.github.io/TgWitness/docs/archive/) · [維基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

從 TgWitness 專案目錄安裝可選的伺服器：

```
python -m pip install '.[mcp]'
```

在控制面板中，開啟**「整合」→「MCP」**。為連線命名、選取其 工作區與聊天室，並設定有效期限。請將存檔憑證複製一次；該憑證 日後無法重新取得。若遺失憑證，請撤銷並發行替代憑證。控制面板憑證與 Telegram 憑證並非 MCP 憑證。

## 連接客戶端

該面板會根據 其[文件中記載的設定](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)，為 **VS Code Local 框架**產生 `.vscode/mcp.json`。 將下載的檔案儲存至該位置，執行 **MCP：List Servers**，並啟動 TgWitness。VS Code 會透過密碼輸入視窗提示輸入憑證。下載的 JSON 檔案僅包含提示參考資訊，而非憑證本身。請使用安裝有 MCP 擴充套件之環境中的 Python 可執行檔。

針對其他 stdio 客戶端，請執行：

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

請在客戶端的受保護環境中設定 `TGWITNESS_ARCHIVE_TOKEN`。請勿將其 放入命令列參數或 URL 中。橋接器透過控制面板的授權 存檔 API 讀取資料；它無法直接存取資料庫。標準輸出僅傳輸 MCP 訊息。

對於遠端客戶，請在控制面板旁執行此服務：

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

透過 HTTPS 反向代理將 `/mcp` 轉發至 `127.0.0.1:8766/mcp`，同時保留 `Authorization: Bearer …` 標頭。停用授權標頭 以及請求／回應正文的記錄。僅在必要時進行超出迴圈連接的綁定，使用 `--host` 和 `--public-url`。此端點採用官方 [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 中的 Streamable HTTP。 它支援明確配置的 Bearer 憑證，但不支援 OAuth 發現機制； 僅需 OAuth 的客戶端不被支援。

**執行檢查協定並進行存取**初始化後，系統會啟動一個真實的 MCP 客戶端並列出可用工具。此過程 不會擷取訊息。進行遠端檢查時，所選的 MCP 伺服器將接收 存檔憑證。請僅將此權限範圍配置給您自行營運或信任的伺服器。

## 範圍與成果

可用工具：`list_workspaces`、`list_chats`、`search_messages`、 `get_message_versions`、`get_message_context`、`get_journal_event` 及 `get_capture_status`。本工具不提供 Telegram 操作、設定變更或 批次匯出功能。 每次讀取都會重新驗證工作區／聊天室的存取權限；已過期或遭撤銷的 憑證將停止運作。限制包括：每份憑證每分鐘 60 次 API 請求、 每頁 50 筆記錄、64 KiB 的回應大小，以及 8 秒的 API 超時限制。

訊息結果包含工作區、聊天/訊息 ID、事件序列、儲存的雜湊值， 以及面板連結。開啟連結的檢視者必須擁有自己的授權面板 會話。原始 Telegram 物件、存取雜湊值、檔案參照、會話資料， 以及金鑰均不予顯示。搜尋功能檢索的是訊息文字，而非原始欄位。 文字內容 會被截斷，並標示截斷處。編輯紀錄、Telegram 刪除通知及 `missing_on_recheck` 仍屬獨立的觀察項目。僅限聊天室範圍的存取權限無法查看 工作區範圍內的運作事件；擷取狀態會明確標示此限制。

存檔中的文字屬於不可信的輸入。訊息內的指示不會賦予任何額外 權限，且不得視為客戶端指令。外部 AI 模型可能會 接收其 MCP 客戶端所請求的任何內容。唯讀存取權限可防止 存檔內容被修改；但無法阻止客戶端保留其讀取的資料。

這些雜湊值用於識別已儲存的記錄，並支援完整性檢查。它們並不能 獨立證明 Telegram 訊息的發送者身分，亦無法證明每則訊息均已被完整擷取。
