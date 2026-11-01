# 快速入門

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/quickstart/

安裝與啟動 TgWitness 的各種方式：Windows 套件、Python、Docker 以及合成示範，並包含初步檢查步驟。

**英文** · [俄語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [烏克蘭語](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [西班牙語](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [葡萄牙語（巴西）](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [土耳其語](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [阿拉伯語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [波斯語](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [烏爾都語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [印地語](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [印尼語](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [越南語](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [簡體中文](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness 是一款用於監控您帳戶可存取之 Telegram 群組與頻道的獨立應用程式， 它於本地端運行，並擁有專屬的資料目錄。

**初次造訪？**請先[瀏覽示範版本](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/quickstart/#explore-the-interface)，再進行帳戶連結。 [請選擇相關指南](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)，內容涵蓋代理伺服器、Witness、資料匯出或伺服器設定。

## 安裝與啟動

[透過 GitHub Actions 擷取（預覽版）](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

請選擇一種方式。可攜式下載檔將於發行版本發布後提供：

| 主機 | 無需安裝任何軟體 | 來源：Python 3.11+ | Docker：Engine/Desktop 搭配 Compose 2.20 以上版本 |
| --- | --- | --- | --- |
| Windows | 從 GitHub Releases 中提取 `TgWitness-<version>-windows-amd64-portable.zip`，雙擊 `TgWitness.cmd` | 雙擊 `Start.cmd` | 雙擊 `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

若採用原始碼方式，請[下載並解壓縮目前的 `main`](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip)，或複製儲存庫：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

如果找不到合適的 Python，`Start.cmd` 會提議為您的 Windows 使用者安裝 Python 3.12（透過 winget 或經過簽署的 python.org 安裝程式）。若缺少 Python，`start.sh` 會印出適用於您的 Linux 發行版或 macOS 的確切安裝指令。首次從原始碼啟動時，會自動建立 `.venv` 並安裝相依套件。

Docker 會編譯應用程式並在背景中啟動它；無需主機端的 Python 環境。 當容器運作正常時，`scripts\Docker.cmd` 和 `scripts/docker-start.sh` 會輸出控制面板位址與代幣。 在所有受支援的主機上，對應的 Docker 指令如下：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

開啟 **http://127.0.0.1:8787**。使用 Docker 輔助程式或第二個 Docker 指令所產生的憑證，或針對可攜式或原始碼安裝版本，從 **data/live/panel-token.txt** 讀取憑證。接著請前往 下方的「**連線至 Telegram」步驟**。 原生安裝與 Docker 安裝使用各自的儲存空間； 啟動 Docker 並不會匯入現有的原生日誌。

針對伺服器，[部署](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/)內容涵蓋自動啟用 HTTPS、重新啟動、 發佈的圖片、更新及備份。

## 探索介面

1. 請在可攜式套件中執行 **TgWitness-Demo.cmd** ，在 Windows 原始碼 資料夾中執行 **scripts\Demo.cmd** ，或在 Linux/macOS 上執行 `sh start.sh --demo` 。首次從原始碼啟動時，系統會先建立 `.venv` 並安裝依賴項。
2. 開啟 **http://127.0.0.1:8787**。
3. 本地示範版本會自動開啟範例日誌。無需複製存取憑證即可直接進行本地存取。

示範訊息均為虛構。示範模式無法連線至真實的 Telegram 帳號。

## 連接 Telegram

> [!警告] **請勿使用任何您無法承受損失的資源。**我們強烈建議您不要連結 個人或重要帳戶，也不要在您重視的帳戶上建立 API ID / 雜湊值。 Telegram 會不預警且經常永久封禁帳戶，無論使用何種客戶端。 測試能否順利進行取決於 Telegram 本身，而非 TgWitness，且無法保證後續運作的穩定性。

1. 若原生示範程式正在執行，請停止它並執行 **Start.cmd** 或 `sh start.sh`。 否則，請讓上述啟動的即時安裝版本繼續運行。
2. 請使用您所採用安裝方式對應的控制面板代碼來開啟控制面板。
3. 若您需要使用代理伺服器，請前往「**帳戶**」**→「設定」→「連線設定」→「變更連線路徑」**進行設定。
4. 在「**帳戶**」中，輸入您的電話號碼並按下「**繼續**」，選擇 **「QR 碼」→「顯示 QR 碼**」，或選取檔案並按下**「連結帳戶」**。 **API ID + Hash** 為選填項目：工作區會使用其儲存或匯入的配對組合， 或從內建池中選取一組可用的配對組合。若要使用您自己的應用程式，請將一組 `API ID:API Hash` 配對組合貼上至 API ID 欄位。 若需完整的授權金鑰，請選擇**「授權金鑰**」，貼上全部 512 個十六進位 字元，並選取提供的 DC ID。使用者 ID 為選填項目，若輸入則會被勾選。
5. 請完成您所選的登入方式：手機號碼／驗證碼／雙因素驗證（2FA），或透過 已登入的 Telegram 應用程式掃描 QR 碼進行確認，亦可匯入受支援的授權會話。
6. 請確認顯示的帳號 ID。開放**來源**：您的聊天記錄會自動載入；請手動新增您的群組。
7. 在「**選擇要保留的變更」**下，請選取事件類別或「 **訊息、編輯與刪除**」預設值，然後儲存監控設定。
8. 請分別選擇附件設定，然後按下「**開始監測**」。

API 憑證用於識別您的應用程式；它們本身並不會 授權任何帳戶。私人群組無需公開使用者名稱，但您的帳戶必須具備存取權限。

對於現有帳戶，請參閱[帳戶與工作階段格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/)：面板接受 Telethon StringSession、Telethon/Pyrogram SQLite、單一帳戶 TData ZIP，以及受支援的帳戶 JSON。請同時選取工作階段及其隨附的 JSON，然後按下**連結帳戶**。也可以使用相同的選用 API 設定進行 QR 碼登入。不支援 TDLib、機器人工作階段，以及 CSV/JSON 帳戶清單。

若有多個帳戶，請使用**帳戶 → 匯入帳戶**並選取其受支援的工作階段檔案。隨附的 JSON 檔案會依主檔名自動配對；每個匯入的帳戶都會獲得各自的工作區。請參閱[大量匯入與帳戶群組](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#bulk-import-and-account-groups)。

若要新增另一個帳戶，請按帳戶選擇器旁的 **+**，或開啟 **「帳戶」→「設定」→「連線設定」→「工作區」**，亦可使用**「帳戶」功能**。各工作區擁有獨立的會話、 日誌、金鑰、來源及佇列。切換檢視畫面時，其他資料擷取程式仍會繼續執行。 在此安裝環境中，同一個 Telegram 帳戶無法指派給兩個工作區。 工作區數量沒有限制；由於它們共用同一個程序，因此容量取決於電腦的效能。

即時面板代幣用於保護您對 Telegram 授權及儲存 資料的存取權限；它與 Telegram API 憑證是分開的。僅有明確啟動且 直接存取的本地示範版本才會自動獲得存取權限。遠端／透過代理伺服器存取的示範版本仍會使用 `data/demo/panel-token.txt`。

## 檢視與匯出

- **日誌：**可依來源及事件類型搜尋並篩選觀察記錄。
- 選擇一項事件，以檢視其原始記錄、來源資訊及儲存的版本。
- 編輯詳情會顯示可用的「編輯前」與「編輯後」內容。刪除詳情則會顯示 最後擷取的內容（如有）；若為未知行為者，其身分仍屬未知。
- **匯出格式：**簽名 ZIP、JSONL、CSV 及離線 HTML。
- **完整聊天記錄匯出**（來源 → 完整聊天記錄匯出）：將單一聊天室的完整可見 歷史記錄下載為包含 `chat.json`（Telegram-export 風格）及可讀取 `chat.html` 的簽名封裝檔。若該帳號為群組成員，則可匯出私人聊天記錄。此為當前的 快照，並非已刪除或先前編輯過的訊息之重建。 使用 `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256` 驗證 副本。
- **儲存檢查點：**將簽名日誌的邊界維持在收集器之外。
- **下載簽名執行收據：**保留收集器的程式／版本記錄。
- **準備時間戳記請求：**向時間戳記授權機構提交離線請求； 請參照 [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/timestamp/) 文件以取得並驗證回應。
- **驗證日誌：**檢查事件簽名與鏈結。ZIP 匯出功能亦會檢查媒體檔案。

受支援的瀏覽器可將大型匯出檔直接儲存至指定檔案。其他瀏覽器 最多僅能緩衝 128 MiB。當伺服器正在運行時，串流命令列介面 (CLI) 支援 更大容量的下載，且無需緩衝整個回應：

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

若要新增另一個工作區，請透過「**匯出」→「工作區 ID」**新增 `--profile ID`。 若要新增遠端伺服器，請新增 `--url https://your-server`。預設傳輸限制為 5 GiB；`--max-mib` 可變更此限制。簽名 ZIP 內容預設另有 4 GiB 的未壓縮 驗證限制（可透過**「參數」**提高此限制；請使用 `verify.py --max-gib N` 驗證此類檔案）。請使用可信賴的驗證器副本以及 獨立保存的金鑰指紋／檢查點來驗證該檔案。

## 查看安裝說明

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` 會偵測本地依賴項、簽名支援、儲存空間、金鑰設定以及 監聽位址。此工具不會安裝任何軟體，也不會連線至 Telegram。若端口 處於繁忙狀態，可能表示另有實例正在運行。請改用其他 `--port`，或先停止該實例。

啟動程式會安裝至 `.venv`。輔助的 `python -m tgwitness...` 指令必須 在 Windows 上使用 `.venv\Scripts\python.exe`，或在 Linux/macOS 上使用 `.venv/bin/python`， 除非該環境已啟用。

## 會話、保護與操作

封閉且一致的 Telethon SQLite `.session` 檔案可透過 `python -m tgwitness.sessions account.session --out account.tgwitness-session` 在本地端轉換，隨後 載入至 Account。亦支援直接檔案匯入及 QR 碼登入。有關登入格式、SOCKS5、 HTTP CONNECT、MTProxy 及外部主金鑰的詳細資訊，請參閱 [CONNECTION-SECURITY.md。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/)

**暫停監測**將停止資料收集。鎖定僅會關閉瀏覽器存取權限。 關閉分頁後，收集程序仍會繼續運行。停止該程序才會中斷 資料收集；歷史快照無法還原所有遺漏的編輯或刪除紀錄。 了解[資料收集在事件政策、附件佇列、 帳戶隔離及重新啟動行為方面的運作方式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/)。

會話與機密資料均經過加密。訊息內容、媒體檔案及匯出檔案需儲存於 加密磁碟或磁碟區中。簽名僅能依據可信密鑰驗證資料的完整性； 無法驗證訊息源自 Telegram，亦無法防止由 控制資料收集器及其密鑰的操作者進行偽造。

請參閱 [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/operations/) 了解備份／還原[操作，DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/) 了解託管設定，以及 [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 中的服務範例。已安裝的 控制面板中亦包含一份離線設定指南，網址為 `/guide.html`。

實際的驗證結果與現存的限制 詳載於 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/) 及 [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) 文件中。
