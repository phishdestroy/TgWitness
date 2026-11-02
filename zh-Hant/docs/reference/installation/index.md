# 安裝、驗證與更新

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/installation/

只需一則指令即可安裝、檢查簽名與雜湊值，並更新或移除安裝。

[專案](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [快速入門](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/quickstart/) · [部署](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/)

## 只需一則指令即可安裝

此引導式安裝程式包含一個專屬的 Python 執行環境。日後安裝時請使用相同的網址： 每次發布都會一併更新安裝程式、雜湊值、簽名 及建置資訊。

**Linux / macOS (Bash)：**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

在 Ubuntu 伺服器上，請以 root 身分執行以安裝背景服務。在桌面電腦上， 請以一般使用者身分執行。

**Windows（PowerShell 或 命令提示字元）：**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

在 Windows 系統上無需管理員權限。子 PowerShell 程序會讓您的 終端機保持開啟狀態並顯示結果。Python 及其依賴項會保留在安裝目錄中。

在 Ubuntu 上，請選擇「**這台電腦**」、「**臨時 HTTPS 連結**」或「**自有網域**」。 安裝程式會顯示控制面板地址和存取金鑰。若要取得臨時連結，請在瀏覽器中開啟 該 HTTPS 地址並輸入金鑰。若需透過遠端 伺服器進行本地存取，請從您的電腦使用 SSH 轉發 (`ssh -L 8787:127.0.0.1:8787 user@server`) 並開啟 `http://127.0.0.1:8787`。在 macOS 和 Windows 上，本地面板會直接在您的 瀏覽器中開啟；請保持其終端機持續運行。

請在面板中登入 Telegram，並選擇要收集的內容。僅進行安裝 並不會啟動 Telegram 資料收集功能。

## 一切運作之處

`get.destroy.tools` 是一個**用於提供靜態檔案下載的 Cloudflare Worker**。它沒有 TgWitness 面板、Telegram 會話或使用者證據資料庫。它不會被路由至 專案的 VPS。該應用程式運行於您執行該指令的機器上。

| 安裝 | 程式 | 資料 |
| --- | --- | --- |
| 以 root 身分使用 Ubuntu | `/opt/tgwitness` | 系統服務： `/var/lib/tgwitness-<installation ID>`；請使用 `tgwitness paths` 以獲取確切路徑。 |
| Linux / macOS 使用者 | `~/.local/share/tgwitness` | `data/live` 在該安裝環境下。 |
| Windows 使用者 | `%LOCALAPPDATA%\TgWitness` | `data\live` 在該安裝環境下。 |

設定 `TGWITNESS_INSTALL_DIR` 以選擇另一個資料夾。已安裝的版本與資料 是分開儲存的。安裝程式不會將您的帳號、訊息或金鑰上傳至 下載網站。選擇 Cloudflare 隧道會將控制面板的流量導向 Cloudflare；使用您自己的網域則會指向您自己的伺服器。

每個安裝包均包含 **START-HERE.html** 和 **START-HERE.txt** 檔案，其中載有本機 路徑、指令以及儲存庫連結。執行 `tgwitness guide` 以開啟指南。 在 Windows 上，請使用 `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` 在 PowerShell 中執行。

## 執行前請先驗證

這條單行指令會信任 HTTPS 上的初始腳本。該腳本會在安裝前檢查 SHA-256 以及應用程式和限制條件上的專案 RSA 簽名。 您也可以先下載並驗證初始腳本。

公開發佈金鑰為 [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub)。 其 SHA-256 為：

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

請保留此來自您信任的儲存庫版本的指紋。來自 同一下載伺服器的校驗和可偵測不一致；而獨立受信任的公開 金鑰則是驗證發行簽名的依據。

請為以下驗證下載內容使用一個新的、空的目錄。

**Linux / macOS — 請在新的、空的下載目錄中執行**（需安裝 curl 和 OpenSSL）：

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

若 `&&` 若下載、金鑰指紋或簽名 驗證失敗，執行鏈將在執行前中止。若在下載腳本與其 簽名之間發生發布更新，請重新下載兩者。舊版安裝程式會保留其不可變的套件 URL。

**Windows — 執行前請檢查 SHA-256：**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

將雜湊值與 `install.ps1` 該行進行比對。若要進行獨立的簽名驗證， 請使用 OpenSSL（例如透過 Git Bash）並採用上述相同的公鑰指紋：

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Windows 安裝程式會透過 .NET 自行驗證套件簽名，無需 OpenSSL。這些是獨立的 RSA-3072 / SHA-256 簽名，而非 Authenticode。 [清單檔案](https://get.destroy.tools/manifest.json)記錄了軟體版本、 精確的 Git 提交碼、不可變的發行 ID 以及每個建構產物的 SHA-256。該頁面連結 至對應的原始碼。清單檔案和校驗和清單也具有獨立的 簽名（`manifest.json.sig` 以及 `SHA256SUMS.txt.sig`).

## 更新現有安裝

**新發布的版本會更新下載網站；當您 再次執行安裝程式時，已安裝的程式便會更新。**本工具不提供無人值守的更新程式，也不會自動重新啟動 正在運行的集合。當前的安裝程式通道為**預覽版**；它遵循 來自 `main`發布並經過驗證的建置版本，其提交時間可能比上一個 編號的 GitHub 發行版更晚。該頁面的版本來自 `pyproject.toml`；其提交 與建置 ID 用於區分同一預覽版本內的更新。

請使用與先前相同的安裝資料夾及作業系統使用者。在停止資料收集時，備份完整的資料 目錄； `tgwitness paths` 以識別該資料夾。經簽名的匯出檔 並非完整的安裝備份。

**Ubuntu 根目錄安裝位於 `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

安裝成功後：

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

若為 Linux/macOS 用戶安裝，請使用原始 `TGWITNESS_INSTALL_DIR` 或 預設設定，並再次執行第一個安裝指令。更新前請先關閉前台 面板，更新後再重新啟動。若為已設定的 Linux 使用者 服務，請執行其 `tgwitness restart` 指令。

**Windows：**關閉正在運行的面板，再次執行 Windows 安裝指令， 然後在 `bin\tgwitness.cmd` 同一安裝環境中執行。安裝程式會保留資料、 工作階段、存取設定及簽名金鑰。僅當 新環境通過檢查後，才會切換啟動器；若安裝失敗，則 原有的啟動器仍會保留。請保留升級前的備份，以因應儲存格式變更。

## Ubuntu 上的常用指令

| 指令 | 結果 |
| --- | --- |
| `tgwitness open` | 當前面板網址與存取金鑰。 |
| `tgwitness paths` | 精確的程式、資料及指南路徑。 |
| `tgwitness guide --print` | 離線操作說明。 |
| `tgwitness status` / `tgwitness logs` | 可用性／服務日誌。 |
| `tgwitness stop` / `tgwitness start` | 停止／恢復服務；保留資料。 |
| `tgwitness token rotate` | 替換管理員金鑰並結束瀏覽器會話。 |
| `tgwitness tunnel off` | 停用公開快速隧道；保留本地面板。 |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | 建立快速隧道連結／替換其網址。 |

請參閱[「存取權限」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/) 以了解同事憑證、會話及 IP 限制，以及 「[安裝程式發佈」](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) 以了解從 GitHub 到 Cloudflare 的發佈工作流程。

## 移除 TgWitness

本工具無專用解除安裝程式：請先停止面板運作，再刪除其資料夾。刪除 data 資料夾將永久銷毀日誌、簽名金鑰、Telegram 連線紀錄及儲存的檔案。 執行此操作前：

1. 匯出您所需的內容（**匯出 → 下載已簽名的 ZIP**），並將簽名金鑰 的指紋與檢查點存放在這台機器之外。若要保留工作區本身，請在停止資料收集後， 複製整個資料資料夾。
2. 請從「**您的伺服器」**中刪除在「**附加功能 → 24/7 伺服器」**下建立的伺服器，或透過 `python -m tgwitness.cloud destroy`；服務供應商將持續向您收費，直至該伺服器被刪除為止。
3. 請在 Telegram 的**「設定」→「裝置」**中結束每個帳戶的會話。刪除 檔案並不會在 Telegram 端登出該會話。

**Ubuntu 根目錄安裝。**請注意資料夾位置，停止服務，然後移除 該服務、相關資料夾及捷徑：

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Linux 或 macOS 使用者安裝說明。**關閉面板。已設定的 Linux 使用者服務 將透過 `systemctl --user disable --now tgwitness-<ID>`；其單位為 `~/.config/systemd/user/`。接著刪除 `~/.local/share/tgwitness` （或您的 `TGWITNESS_INSTALL_DIR`) 以及 `~/.local/bin/tgwitness` 捷徑。

**Windows。**關閉面板並刪除 `%LOCALAPPDATA%\TgWitness` （或您的 `TGWITNESS_INSTALL_DIR`)。安裝程式不會新增任何服務、排程任務或捷徑。
