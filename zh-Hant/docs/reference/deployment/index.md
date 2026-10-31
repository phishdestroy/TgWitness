# 部署

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/

可在 Windows、Linux、macOS 或 Docker 環境中，透過 HTTPS 運行 TgWitness 服務，並具備備份與更新功能。

**英文** · [俄語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [烏克蘭語](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [西班牙語](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [葡萄牙語（巴西）](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [土耳其語](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [阿拉伯語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [波斯語](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [烏爾都語](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [印地語](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [印尼語](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [越南語](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [簡體中文](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## 選擇安裝方式

若要取得可攜式套件，請從 GitHub Releases 解壓縮 `TgWitness-<version>-windows-amd64-portable.zip`。若採用其他方法，請下載並解壓縮原始碼 ZIP 檔，或克隆 儲存庫，然後在專案目錄中執行以下指令：

| 安裝 | 開始 | 會在背景執行嗎？ |
| --- | --- | --- |
| Windows 便攜版套件 | `TgWitness.cmd` | 不；請保持視窗開啟。 |
| 原生 Windows 版本 | `Start.cmd` | 不；請使用可選的登入任務以進行背景運作。 |
| 原生支援 Linux／macOS | `sh start.sh` | 不；請使用 systemd/launchd 進行背景執行。 |
| 在任何受支援的主機上運行 Docker | `docker compose up -d --build --wait` | 是的，只要 Docker 守護程式正在運行。 |
| Windows 版 Docker 輔助工具 | `scripts\Docker.cmd` | 是的；該輔助程式會監控網頁伺服器的運作狀態。 |
| 適用於 Linux/macOS 的 Docker 輔助工具 | `sh scripts/docker-start.sh` | 是的；該輔助程式會監控網頁伺服器的運作狀態。 |

若需部署可由第三方驗證的雲端伺服器——該伺服器透過 服務供應商的 API 建立，不使用 SSH，且僅能透過 Cloudflare Tunnel 存取——請參閱 [「高保障部署](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md)」說明。

原生啟動程序會建立一個私有 `.venv`，並安裝已固定（pinned）的依賴項。 Docker 會在映像檔內建置這些組件，無需主機端的 Python。首次 設定需要網路連線。 若未偵測到 Python 3.11 以上版本，`Start.cmd` 會先徵求確認， 再為當前 Windows 使用者安裝 Python 3.12（若使用 winget，否則在驗證 Python 軟體基金會簽章後， 將使用 python.org 安裝程式）；此過程絕不會要求 管理員權限。Docker 及作業系統服務仍為先決條件。

原生及可攜式安裝會在其資料夾內使用 `data/live`。Docker 則使用名為 `tgwitness-data` 的卷 ，位置為 `/data`。在您刻意遷移 完整資料目錄之前，這兩者屬於獨立的安裝。請勿預期新的 Docker 容器會自動偵測到原生 帳戶。

## 安裝需求

原生安裝需具備 Python 3.11 或更新版本，並包含 `venv` 和 `ensurepip`；首次安裝依賴項時需有網際網路 連線，且需為 `.venv` 準備可寫入的專案目錄。內建的控制面板無需 Node.js 或前端建置。請從 您的一般作業系統帳戶執行啟動程式；TgWitness 無需管理員／root 權限。

- **Windows：**`Start.cmd` 會先檢查 `py -3`，接著檢查 `python`，然後檢查預設的「使用者專用」及 「Program Files」安裝資料夾，並需要 3.11 版或更新版本。若以上皆無法運作，它 會提供上述所述的自動「使用者專用」安裝選項。`py -3 start.py` 亦可運作。 可攜式套件完全不需要 Python。
- **Linux：**`start.sh` 會依序嘗試 `python3.13`、`python3.12`、`python3.11`、`python3` 及 `python`，若均不符合條件，則會輸出適用於 apt、dnf、pacman、zypper、apk 或 Homebrew 的安裝指令。 Debian/Ubuntu 系統的安裝可能需要與所選解釋器相符的 `python3-venv` 套件。 發行版的舊版 預設 Python 必須被 Python 3.11 以上版本取代或補充。
- **macOS：**請安裝最新的 Python 3.11+ 發行版；請勿假設作業系統預設提供的 解釋器符合要求。請使用專案目錄中的 `python3 start.py`。
- **Docker：**請使用搭配 Compose v2.20 或更新版本的 Docker Engine／Desktop。在 Windows 系統上，Docker Desktop 必須使用 Linux 容器。該容器會自行安裝 所需的 Python 依賴項；主機無需另行安裝 Python。

請使用持久性本地儲存空間作為資料目錄。規劃容量時需考量訊息、 媒體檔案、WAL 增長、匯出及備份等因素；目前尚無基於實證的通用最低 磁碟／記憶體規格適用於所有工作負載。若 CPU 架構與 Python 版本 缺乏相容的依賴項輪（wheel），可能需要額外的建置工具及其 專屬的驗證程序。 「可攜式」並非指聲稱支援所有作業系統或硬體。

已於本地端驗證 Windows 11/Python 3.12 環境。Linux/macOS/容器設定檔及持續整合 (CI) 雖已提供，但尚未在此開發主機上執行。具體範圍請參閱 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/) 檔案。

## 本地電腦

請在 Windows 系統上使用 `Start.cmd`，或在 Linux/macOS 系統上使用 `sh start.sh`。`scripts\Setup.cmd` 或 `sh start.sh --setup-only` 會預先 設定環境。啟動程式在首次使用時會安裝所需依賴項；後續啟動時 則會重複使用該環境。設定及 Telegram 訊息收集過程需要網路連線， 但瀏覽現有記錄及建立匯出檔則可在離線狀態下進行。

設定完成後執行 `python start.py --check`，以檢查本機依賴項、Ed25519、 儲存空間、金鑰設定及監聽位址，此過程不會啟動資料收集器。 若需結構化輸出，請使用 `--json`。傳入預期的 `--data-dir`、`--host` 及 `--port`。此檢查不會安裝套件、建立日誌或連線至 Telegram； 亦非完整性或覆蓋範圍的驗證。啟動時會另行驗證 現有日誌。`python start.py --help` 亦會跳過安裝步驟。

選項：

執行 start.py 後，請在 Windows 系統上使用 `.venv\Scripts\python.exe`，或在 Linux/macOS 系統上使用 `.venv/bin/python` 來執行輔助指令，亦可先啟用該環境。 以下 `python -m ...` 範例假設該環境已啟用。

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

環境變數：TGWITNESS_DATA、TGWITNESS_HOST、TGWITNESS_PORT、TGWITNESS_TOKEN。 TGWITNESS_VAULT_KEY_FILE 用於在新安裝時選取外部金鑰模式；詳見下文。 若提供 TGWITNESS_TOKEN，其長度必須至少為 24 個字元；請使用加密級 隨機值。若未提供，應用程式會於 panel-token.txt 檔案中產生一個 256 位元的隨機憑證。 環境變數的覆寫設定不會重寫該檔案。請重新啟動以輪替憑證。

僅允許一個進程擁有資料目錄。跨平台作業系統檔案鎖定機制可防止 意外的並發寫入。請使用一個 Uvicorn 工作程序。控制面板可管理任意數量的 工作區，額外的工作區目錄位於 profiles/<id>/ 之下。 若需獨立的服務實例，請使用獨立的目錄與埠號。SQLite WAL 檔案應存放於本機持久性 儲存裝置，而非網路檔案系統。請勿在複本之間共用同一個卷宗。

## Windows 便攜版套件

每個 GitHub 發行版本均包含 `TgWitness-<version>-windows-amd64-portable.zip` 及其 `.sha256`。其中包含來自 python.org 的官方可嵌入式 Python 3.12 執行環境 （校驗和固定於 `tools/build_portable.py` 中）、TgWitness 及其固定依賴項， 以及三個啟動程式：

| 檔案 | 目的 |
| --- | --- |
| `TgWitness.cmd` | 啟動控制面板；額外選項將被直接傳遞，例如：`TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | 在 `data\demo` 啟動合成示範 |
| `TgWitness-Check.cmd` | 在不啟動的情況下執行就緒檢查 |

將整個壓縮檔解壓縮至可寫入的資料夾（例如 `Documents\TgWitness`）；請勿 直接從 ZIP 檔案內部或 Program Files 資料夾執行。執行環境採用隔離的模組路徑， 因此其他 Python 安裝程式及 `PYTHONPATH` 皆不會影響其運作。 資料會儲存於 套件的 `data` 資料夾中。若要更新，請先停止 TgWitness，將新版本解壓縮至新的 資料夾，並將 `data` 資料夾複製過去。

請在 64 位元 Windows 系統上使用 Python 3.12 自行建置：

```
python tools/build_portable.py
```

建置程式會驗證執行時校驗和，將受限的依賴項安裝至 套件中，使用內嵌的解釋器執行就緒檢查，並將 ZIP 檔案 與校驗和寫入 `dist/`。

## 容器

```
docker compose up -d --build --wait
```

此操作將為 /data 建立一個命名持久化卷。 網頁埠號已映射至 127.0.0.1:8787。 該程序以 UID 10001 執行，並具備 已撤銷的權限、唯讀的根檔案系統，以及可寫入的 /data 和 /tmp 目錄。 `--wait` 會在返回前檢查網頁伺服器的運作狀態；它不會建立 Telegram 授權或傳送連線。 提供的輔助程式在建置完成後，會採用 180 秒的就緒超時設定； 初始依賴項的下載時間可能比這更長。

兩個基礎 Compose 檔案均使用專案名稱 `tgwitness`，因此將新版本 解壓縮至其他目錄時，系統不會自動選取新的資料卷。請僅保留一個 該專案的部署處於活躍狀態。若為獨立安裝，請使用唯一的 `docker compose -p NAME ...` 以及不同的主機埠，並在更新時保留兩者。 若為使用不同專案名稱的舊版部署，請繼續使用其原始 名稱並搭配 `-p`；`docker compose ls` 會列出現有專案。

將 `deploy/env.example` 複製到 `.env`，並將 `TGWITNESS_PORT` 修改為使用不同的迴路 埠。例如，`TGWITNESS_PORT=8788` 會將控制面板公開於 `http://127.0.0.1:8788`；容器仍會監聽 8787 埠。`.env` 已被 Git 忽略。

取得初始代幣：

```
docker compose exec tgwitness cat /data/panel-token.txt
```

實用指令：

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` 會在發生當機或 Docker 守護程式 重新啟動後，重新啟動資料擷取器。在 Linux 伺服器上，請使用您所使用的發行版的服務 管理程式（通常為 `sudo systemctl enable --now docker`）啟用開機自動啟動 Docker。在 Windows/macOS 上，請啟用 Docker Desktop 的「登入時啟動」設定。當桌面登出、進入睡眠狀態，或 Docker Docker 守護程式都可能中斷資料收集。明確停止的容器將保持 停止狀態，直到您再次啟動它為止。

在範例配置中，/tmp 卷的上限為 512 MiB。匯出機制 改為使用各工作區的 `temporary-exports/` 存於持久化 /data 目錄中。請在該處預留空間 以因應同時進行的匯出作業、日誌/WAL 增長、媒體檔案及備份需求。 啟動程式使用 deploy/constraints.txt 來鎖定符合資格的執行時依賴項版本。 Docker 及高保障等級伺服器會依據 deploy/requirements.lock 和 deploy/build.lock 透過 pip --require-hashes 進行安裝：每個套件檔案必須與提交紀錄中 的 SHA-256 值相符，因此若檔案在 PyPI 或鏡像站點上被替換，系統將拒絕該檔案。 Python 基礎 映像及作業系統套件仍需經過獨立的版本認證。

除非您打算銷毀日誌和金鑰，否則請勿使用 `docker compose down -v` 指令。 容器狀態報告僅顯示網頁伺服器的可用性，而非 Telegram 擷取是否成功。 請檢查控制面板中的收集器狀態、心跳訊號、錯誤及覆蓋事件。

### 獨立見證者簡介

可選的 `witness` 服務會在獨立的 容器中運行一個[獨立的見證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/)實例，該實例在 `witness-data` 卷中擁有專屬的金鑰和日誌，而收集器僅擁有 只讀的見證代幣。請在控制面板的**「見證」**頁面建立該代幣，並將其 連同機器人代幣和頻道一併新增至 `.env`，然後啟動該設定檔：

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

此服務可透過 Compose 網路內的收集器存取，網址為 `http://tgwitness:8787` （`TGWITNESS_WITNESS_COLLECTOR` 會覆寫此設定，例如 `/profiles/<workspace ID>` 適用於 另一個工作區）。若要使用由他人運作的獨立伺服器上的證據日誌，請在該處使用 `deploy/compose/compose.witness.yaml` ，並將 `TGWITNESS_WITNESS_COLLECTOR` 設定為收集器的 HTTPS 位址；該檔案僅包含證據日誌。

## 安裝已發佈的映像檔

此網站將於[發布工作流程](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/#automated-github-releases) 成功完成，且 GHCR 套件配置公開後正式上線。儲存庫的所有者／名稱並未硬編碼 於此原始碼樹中。請使用該次發布工作流程摘要中顯示的圖片。

將 `deploy/env.example` 複製到 `.env`。將 `TGWITNESS_IMAGE` 設定為已發布的版本，並使用 **小寫的**儲存庫路徑，例如：

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

請直接執行此檔案，而非執行 ``compose.yaml``：

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

主機端無需進行原始碼編譯、Python 環境或編譯器。發行工作流程 針對 Linux AMD64 和 ARM64 容器，包括 Docker Desktop 的 Linux 虛擬機器。 請使用版本標籤或工作流程摘要中的「`ghcr.io/owner/repository@sha256:...`」。 未配置動態標籤「`latest`」或無人值守的應用程式升級。當 專案名稱相同時，映像檔與原始碼變體將共用同一個資料卷。

## 伺服器上的自動 HTTPS 功能

請使用配備 Docker 的伺服器、您所掌控的網域，以及持久的本地儲存空間。 將網域的 A/AAAA 記錄指向該伺服器；僅當 IPv6 可連達該伺服器時，才發布 AAAA 記錄。 允許傳入的 TCP 80 和 443 連接，以及用於憑證簽發的傳出 DNS/HTTPS 連線。 其他服務不得已佔用這些埠號。

將 `deploy/env.example` 複製到 `.env`，並設定主機名稱（不包含方案或路徑）：

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

使用 HTTPS 覆蓋層開始建置原始碼：

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

若要發布圖片，請改以 `deploy/compose/compose.image.yaml` 作為第一個檔案。請保留 兩個 `-f` 參數，以便日後執行狀態查詢、日誌檢視、更新及停止指令。

Caddy 負責取得並更新憑證、將 HTTP 重定向至 HTTPS，並將 請求轉發至私有 Compose 網路上的收集器。憑證狀態 擁有專屬的持久化儲存區。收集器的直接主機埠僅限於迴路連接。 提供的 Caddy 設定未啟用存取記錄功能。

開啟 `https://watch.your-domain.org` 並輸入面板代碼。準備就緒 並不代表已確認憑證已簽發或外部可連通。若 HTTPS 尚未 就緒，請檢查 DNS、防火牆規則，以及：

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

提供的 Caddy 映像檔遵循其 `2-alpine` 標籤。拉取操作會更新該映像檔； 若需固定基礎架構版本，請在您的部署中固定一個已測試的摘要。

## 更新與備份

在更新過程中，請保留 Compose 專案名稱及資料量。首先停止 收集器，並執行完整備份。針對預設的基於來源的部署：

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

每次請使用位於儲存庫之外的新備份目的地，並將其視為 需受帳戶存取權限保護的資料。範例路徑僅供說明；請使用您自己的私人備份 位置。複製整個目錄，包括隱藏檔案、所有工作區、金鑰、 日誌及媒體檔案。若已設定外部金庫主金鑰，請另行備份。 證據 ZIP 檔並非可還原的應用程式備份。若使用 HTTPS，且需保留其憑證／帳戶狀態時， 請一併保留 Caddy 卷宗。

若要進行原始碼部署，請取得最新發行版本的檔案，並執行：

```
docker compose up -d --build --wait
```

若要進行圖像部署，請將 `TGWITNESS_IMAGE` 改為所需版本，然後執行：

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

請亦使用您安裝環境中的 Compose 檔案來執行前述的停止／複製指令。 請保留 `.env`、自訂設定以及相同的專案名稱。`down` 會保留命名 的資料卷；**`down -v` 則會刪除它們**。請勿在不同作業系統 或 Python 版本之間複製 `.venv`。若要進行原生更新，請先停止 TgWitness，備份其完整的資料 目錄，替換原始檔案，並在啟動前執行 `python start.py --setup-only`。

更新後，請檢查控制面板存取權限、帳戶身分、監測狀態及覆蓋範圍。 重新啟動並不會重建遺漏的 Telegram 更新。若未來版本變更儲存格式， 回滾操作可能需要使用更新前的備份。

## GitHub 自動發佈

當此 專案推送至已啟用 Actions 的 GitHub 儲存庫後，[發布工作流程](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml)即已就緒。該流程會在 **發布** GitHub Release 時執行，包含預發布版本。僅推送草稿或標籤 並不會發布套件。

1. 設定套件版本與變更紀錄，然後發布一個標記為 `v` 加上確切 `pyproject.toml` 版本（例如 `v0.7.0`）的發行版本。
2. 此工作流程會驗證標籤，並執行適用於 Windows/Linux/macOS 的共用 Python、 general/account-import/QR 瀏覽器、原始碼套件及 Docker 檢查。此外，亦會在 這三種作業系統上，使用 Python 3.12 進行全新的原生安裝測試。
3. 通過上述檢查後，系統會在 QEMU 環境下對 ARM64 映像檔進行煙霧測試，並將 AMD64/ARM64 映像檔發佈至 `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`， 同時將原始碼 ZIP 檔、校驗和及 Python wheel 檔案附加至發行版本。另有一項 Windows 工作會負責編譯並附加可攜式 ZIP 檔及其校驗和。
4. 首次發佈後，請開啟 GHCR 套件設定，並將可見性 設為「**公開」**，若需進行匿名影像擷取。僅有公開的原始碼儲存庫 並不能保證套件會以公開容器形式發佈。組織政策必須 允許套件發佈。此工作流程使用 `GITHUB_TOKEN`；儲存庫中 不得包含任何註冊表密碼或 VPS 憑證。

此本地準備工作尚未證實遠端工作流程能順利運作。ARM64 模擬僅為初步測試，並非原生硬體或實際 Telegram 環境的驗證。 此功能可自動化版本發佈封裝；啟動伺服器仍需使用 Compose 指令及其網域／主機的先決條件。當新版本發佈時，現有伺服器不會自動 進行升級或重新啟動。

## 遠端伺服器

請將服務限制在迴路連接並使用 SSH 隧道，或讓 HTTPS 連線在 反向代理伺服器處終止。基礎 Compose 檔案僅限本地使用；可選的 `deploy/compose/compose.https.yaml` 覆蓋層會提供 Caddy 以支援已設定的網域。 請勿讓承載者憑證出現在 URL 及代理伺服器日誌中。反向代理伺服器應限制 請求大小與連線頻率。請勿將明文 HTTP 暴露於網際網路。

[deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 目錄中提供了 systemd、Windows 登入任務、macOS 使用者代理程式以及 Caddy 的範例， 請在安裝前檢視並調整其路徑。 這些僅為範本，並非在本地端執行的平台設定。 標準啟動程式不會註冊任何背景服務或任務。

在 Windows 系統上，以無視窗模式啟動 `pythonw.exe` 時，會將啟動／伺服器診斷記錄儲存於 資料目錄下的 `logs/server.log` 中（每檔 5 MiB，包含兩份輪替備份）。 以控制台模式啟動時，則會保留控制台日誌。兩種模式下 皆已停用 HTTP 存取日誌。請透過資料目錄保護日誌，並在分享前進行審閱。

## 重新啟動與資料缺口

系統會保留上次請求的監測狀態。若監測處於活躍狀態， 啟動時系統會嘗試重新連線並恢復已選定的來源。手動暫停會清除 此設定。重啟失敗的紀錄將被保存並顯示於控制面板中。

StringSession 會保留授權狀態，但不會保留 Telethon 的持久性更新／實體狀態。 對話內容會在啟動時重新載入。Telegram／Telethon 能在運行期間恢復部分傳輸中斷， 但 TgWitness 並不保證在程序重新啟動後仍能進行持久性重播。 每次啟動時，系統會記錄前一期的日誌頭部及離線分界點。 監控程式每 10 秒檢查一次連線狀態，並每分鐘發送一次心跳訊號 （**參數 → 存活記錄間隔**）。 短暫的中斷可能無法被偵測到；連線狀態並不能保證 更新訊息的完整傳遞。快照是明確的當前歷史觀察結果，絕非用來填補資料缺口。

媒體佇列儲存於各工作區的 SQLite 資料庫中。訊息及其對應的處理任務 會以原子性方式一併提交。中斷的執行中任務會在啟動時恢復並重新嘗試。 每次下載設有 120 秒的基本超時，外加以 256 KiB/s 速率計算的檔案大小所需時間，且 每種附件類型設有 1–2,000 MiB 的上限；超時、速度與重試次數皆可在**「參數」**中設定。收集器 會跳過大小未知的檔案。暫停操作時，排隊中的工作會被保留。 重試會使用原始的 已觀察到的檔案描述符，絕不會使用後續編輯訊息的最新版本。 暫時性失敗的重試次數有限；媒體 FloodWait 暫停狀態在重新啟動後仍會保留。 媒體恢復與 Telegram 更新恢復是分開的，且無法重建已消失的檔案。

## 備份、還原與儲存容量

在複製**整個資料目錄**（包括 vault.key、 signing.enc、credentials.enc、SQLite 資料庫／WAL 檔案、媒體檔案、代幣、檢查點， 以及所有個人設定檔／子目錄）之前，請先停止該程序。 請在 目標服務停止運作時還原 完整的副本。若金庫金鑰遺失或 簽名金鑰不匹配，將導致啟動失敗；請勿重新產生金鑰以強行存取。

請將秘密備份進行加密並實施存取控制。證據 ZIP 檔具有可攜性， 請檢視的是證據檔案，而非應用程式備份或 Telegram 會話備份。 本工具不具備自動保留與刪除功能。請預留足夠的磁碟空間，以存放所有訊息、原始 元資料、媒體檔案、臨時匯出檔及備份。

啟動驗證並匯出串流記錄，而非載入整個日誌。 匯出操作會鎖定已讀取的快照，同時新的 WAL 寫入仍可繼續；長時間執行的匯出 會保留 WAL 頁面，因此磁碟容量仍至關重要。ZIP 檔案的上限為 4 GiB （未壓縮），以符合獨立驗證者的預設值； **「參數」→「最大簽名 ZIP**」 可提高上限，此類檔案將透過 `verify.py --max-gib N` 進行驗證。其他格式則無事件計數上限。 支援的瀏覽器會將回應片段串流至使用者選定的檔案。其他瀏覽器 最多緩衝 128 MiB，並將較大的傳輸導向經認證的 CLI：

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

若要使用其他工作區，請從「**Exports → Workspace ID**」中選用 `--profile ID`； 若要使用遠端伺服器，請選用 `--format zip|jsonl|csv|html` 或 `--url https://your-server`； 若要變更 5 GiB 的傳輸限制，請選用 `--max-mib`。僅允許在 迴圈連接（loopback）中使用純 HTTP。憑證透過標頭傳輸，拒絕重定向，現有檔案 不會被覆寫，且未完成的下載不會被發布為已完成檔案。 若 TGWITNESS_TOKEN 覆寫了生成的憑證，請使用一個獨立受保護的檔案 來存放該有效值：panel-token.txt 不會因覆寫而被改寫。 該指令的 SHA-256 僅為傳輸校驗和；請獨立驗證已簽名的 ZIP 檔案。

伺服器匯出檔案將保留於各工作區的私有 `temporary-exports/` 目錄中。 成功執行的匯出作業會清理其檔案。中斷的匯出作業將於 下次工作區啟動時移除，屆時該工作區將保持其專屬實例鎖定狀態。此目錄屬於 儲存威脅／容量模型的一部分；請使用加密資料卷。生產級別的 數吉字節級傳輸仍需在您的目標系統上進行驗證。

該面板顯示排隊中／失敗的媒體檔案、最舊的待處理媒體檔案、可用磁碟空間、Telegram 請求暫停狀態，以及存取權限未經確認的來源。這些診斷資訊並非 完整的端對端傳輸監控。工作區共用同一個程序；若某個帳戶活動頻繁， 仍可能影響其他帳戶。 獨立的工作程序、資料保留／輪替、持久性更新 恢復以及完整的部署認證仍維持不變。控制面板的範圍式存取權限已記錄於 [「存取與權限」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/)文件中；獨立檢查點則由「 [見證指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/)」涵蓋。

## 連線與保護選項

連線路徑依工作區而定，應在授權前完成設定。 SOCKS5/HTTP CONNECT 採用固定依賴項 python-socks。MTProxy 則使用 Telethon 的 實驗性隨機化中間傳輸協議；不支援偽 TLS ee 機密金鑰。 直接備用連線取決於所選的 [IP 模式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/#ip-modes)：「隱藏 IP」模式會拒絕此功能；「顯式備用」模式則會在延遲後允許此功能。「隧道/VPN」模式允許直接連線，但不會建立 VPN。此非系統層級的網路政策。

對於新安裝，TGWITNESS_VAULT_KEY_FILE 應指向一個獨立受保護的隨機 主金鑰檔案。請在容器中將其以唯讀方式掛載至 /data 目錄之外。請分別將每個工作區的公開 vault.external.json 鹽值元資料與主金鑰妥善保存。 現有的本地金庫需要進行有計畫的遷移；設定此變數並不會 自動將其轉換。訊息／媒體儲存及匯出內容均未經應用程式加密。 請視需要使用加密卷宗及足夠的私人臨時儲存空間。

詳細操作流程：[連線／安全性](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/)及 [運作模式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/operations/)。
