# 安全性與資料處理

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/

威脅模型、存取模型、靜態機密資料、網路暴露風險、會話匯入，以及如何回報漏洞。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [部署與復原](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/)

![部署與復原](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

本頁說明在本地或伺服器工作區中的存取、儲存及網路保護機制。 若要在 GitHub Runner 或 Intel TDX 機密虛擬機器中進行資料蒐集，請參閱 [驗證模式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope)，該模式會額外對蒐集環境進行檢查。 帳戶連線、通知、時間戳記、異地副本及見證者各有其專屬的路由設定。

| 領域 | 簡而言之 |
| --- | --- |
| 存取 | 管理員金鑰加上對帳戶／聊天室的範圍式存取權限、七項權限設定及可撤銷的連線；預設為 localhost |
| 靜態資料的隱私 | 會話、API 配對、簽名金鑰及代理伺服器設定均採用 Fernet 進行加密 |
| 訊息與媒體 | 資料以未加密形式儲存：請啟用磁碟加密並設定嚴格的存取權限 |
| 完整性 | 每筆記錄均附有 SHA-256 雜湊鏈及 Ed25519 數位簽名 |
| 本地信任邊界 | 主機管理員負責管理工作區及其簽署金鑰；獨立檢查點則保留較早的日誌邊界 |

有關漏洞通報，請參閱[安全政策](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)。

**本頁內容**

- [存取模型](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/#access-model)
- [面板內容與匯出功能](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/#panel-content-and-exports)
- [靜態機密](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/#secrets-at-rest)
- [代理伺服器與網路路徑](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/#proxies-and-network-routes)
- [登入與會話匯入](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/#sign-in-and-session-imports)
- [日誌與傳輸](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/#logs-and-transport)
- [完整性限制](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/#integrity-limits)
- [若您懷疑有問題](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/security/#if-you-suspect-a-problem)

## 存取模式

主控制面板憑證賦予完全控制權。其他使用者可獲得其專屬的 [範圍限定存取權限](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/)：包含指定的工作區與聊天室、權限設定、有效期限、 IP 限制、登入次數限制以及可撤銷的連線。若存取權限僅限於特定聊天室， 即使已勾選相關權限，亦無法執行整個工作區的操作。 工作區共用同一個執行程序，且資料不會與主機管理員隔離。

該面板預設在 localhost 上監聽。透過瀏覽器登入時，系統會將存取 令牌兌換為會話憑證；瀏覽器會將其作為承載者令牌傳送。該令牌儲存於 sessionStorage 中，而非認證 Cookie。鎖定／登出會清除 瀏覽器會話。關閉瀏覽器或結束會話並不會停止資料收集。

已發行的憑證與會話憑據會以雜湊值形式儲存於加密保管庫中。 撤銷憑證將終止相關會話；權限變更則會影響後續 請求。已下載的檔案無法被收回。管理員亦可限制 自身的瀏覽器會話，但直接使用主控制面板憑證的腳本仍可 保留完整存取權限，並繞過這些瀏覽器會話限制。

驗證失敗會根據客戶端位址進行速率限制。IP 限制採用 應用程式所偵測到的位址；在依賴此機制前，請先確認 反向代理伺服器的運作行為。Witness 憑證仍為獨立的唯讀檢查點／狀態憑證。

### 試用存取

`/api/demo-access` 是一個刻意未經身份驗證的引導程式，專用於明確 啟動且隔離的合成示範環境。它會發出一個獨立於進程生命週期的權限， 絕不會發出真實的面板代幣或 TGWITNESS_TOKEN 覆寫代幣。 其發行與使用需具備 迴路對等節點及主機，不得包含轉發標頭，亦不得進行跨來源請求。若存在 其他工作區或已授權的會話，則此路徑將被停用。活躍工作區絕不會 發行此權能。此示範無法連結帳戶或變更資料蒐集設定。

## 面板內容與匯出功能

本頁面未使用任何外部字型、分析工具、CDN 資源或嵌入式遠端媒體。 來自 Telegram 的文字以純文字形式插入，而非 HTML。下載的附件 以二進位附件形式提供。JSONL 匯出檔保留原始字串；HTML 則會對其進行 轉義；可能成為公式的 CSV 儲存格會加上單引號作為前綴。

匯出檔案不包含驗證與簽署密鑰，但會刻意保留 所收集的來源元資料、識別碼，以及可能包含的個人或敏感內容。 原始來源元資料中可能包含 Telegram 存取雜湊值與檔案參照。

## 靜態資料的隱私

Telegram API 憑證、會話金鑰及簽名金鑰均採用 Fernet 進行加密。 針對本機訊息與媒體檔案，其加密由主機的磁碟或磁碟區負責； 工作區則儲存一般檔案。匯出檔案可採用密碼保護的 AES-256 ZIP 格式， 而異地備份則採用 AES-256-GCM 加密。

金庫金鑰預設位於受保護的資料目錄中。請使用下方的外部主金鑰檔案 將其分開儲存。在 Unix 系統上，新的私密金鑰檔案使用權限模式 0600，新的資料 目錄則使用 0700；在 Windows 系統上，請為服務帳戶及 授權管理員設定目錄存取控制清單 (ACL)。現有的目錄權限將予以保留。

### 外部主金鑰

對於新的資料目錄，TGWITNESS_VAULT_KEY_FILE 可提供外部隨機 主金鑰。系統會透過 HKDF-SHA256 及獨立的隨機鹽值，為每個工作區 衍生出不同的 Fernet 金鑰。為確保資料復原，必須保留 vault.external.json 檔案。若主金鑰遺失或 錯誤，系統將無法正常運作。現有的本機金庫不會被自動遷移。 此面板會顯示所選的金鑰儲存模式。無論採用何種模式，磁碟加密皆會保護本機的 訊息與媒體檔案；有關設定詳情，請參閱「 [連線與資料保護」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/)。

## 代理伺服器與網路路由

代理伺服器設定會加密儲存於金庫中。密碼及 MTProxy 機密資訊 不會透過 API 傳回，也不會寫入證據記錄中。每個工作區皆可自行選擇 其 Telegram 路由及 [IP 模式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/#ip-modes)。

**「隱藏地址」**模式會拒絕直接使用 Telegram 備用連線，並要求透過代理伺服器處理外部 HTTP 請求。明確選取的備用模式允許在延遲後直接存取 Telegram； 隧道／VPN 模式則允許直接連線。選擇隧道 模式並不會安裝或驗證 VPN。這些設定不會控制所有裝置 流量、瀏覽器、套件管理員或由本地代理主機進行的 DNS 解析。

MTProxy 僅傳輸 Telegram 流量。外部請求可使用獨立的 SOCKS5/HTTP 代理、工作區的 SOCKS5/HTTP 路由，或允許的直接路由； 亦可將其停用。獨立見證器擁有其專屬的傳輸設定。 一般 SOCKS5/HTTP CONNECT 認證並不會由這些代理 協定本身進行加密。偽造的 TLS MTProxy 密鑰目前仍不被支援。

## 登入與會話匯入

轉換後的 .tgwitness-session 檔案在 載入並儲存至金庫之前，會包含明文授權密鑰。離線命令列介面 (CLI) 接受經過審核的 Telethon 資料結構。 面板匯入功能另支援 Pyrogram SQLite、現代單一帳戶 TData ZIP， 以及已建檔的 JSON 輸入格式。此功能需經身份驗證，限四個檔案／8 MiB， 並在記憶體中處理上傳內容，無需解壓縮存檔或儲存原始檔案。 正規化的憑證僅會回傳給發出請求且已驗證的瀏覽器； 在 Telegram 授權成功後，這些憑證會儲存於加密的保管庫中。 請保護原始檔案與轉換後的檔案，並避免多個客戶端同時複製同一組授權憑證。

資料處理過程會驗證容器校驗和、本地解密雜湊值以及結構 長度。系統會暫時使用使用者提供的桌面版本地通行碼，且不會儲存該密碼。 此有限解析器無法保證所有桌面版皆相容。 QR 圖像在本地端生成，包含短效期的 Telegram 登入憑證，且 絕不會傳送至外部渲染服務。鎖定裝置、切換工作區、重新登入， 以及路由變更都會取消待處理的 QR 嘗試。重新載入或關閉分頁可能會導致 該嘗試維持待處理狀態直至過期。成功的 QR 登入仍會強制執行帳戶綁定。 一般 API 請求體仍限制為 16 KiB；經認證的匯入路徑接受 最多 12 MiB 的編碼 JSON，並會另行強制執行較小的解碼檔案限制。

登入代碼及 Telegram 兩步驟驗證密碼均不會被永久儲存。電話號碼／代碼雜湊狀態僅在 授權期間暫存於記憶體中。Telegram 連線會話賦予帳戶存取權限；切勿 將資料目錄、會話、憑證、金庫金鑰或私人簽署金鑰上傳至 GitHub。

## 日誌與傳輸

預設的 API 驗證回應已進行替換，以避免回傳憑證 值。應用程式存取記錄功能已停用。請勿設定反向代理伺服器 以記錄 Authorization 標頭或請求正文。HTTP 會以明文傳輸憑證 和登入密鑰：只要連線離開 localhost，請務必使用 HTTPS 或 SSH 隧道。

## 完整性限制

本地驗證會檢查記錄簽名、雜湊鏈、附件及匯出清單。 管理員持有本地簽署金鑰，並可建立另一份已簽署的日誌； 獨立保存的檢查點可偵測其所涵蓋的前綴是否遭替換。 請將金鑰指紋與檢查點交由收件者或獨立見證人保管。

若需經過獨立驗證的資料蒐集，請選擇 [GitHub Actions 擷取](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) 或 [Intel TDX 部署](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)。 其驗證器除檢查檔案庫完整性外，還會驗證工作流程的來源追溯性或硬體測量結果。 可選的時間戳記與加密的異地副本可提供時間錨點及可恢復的副本； [證據格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope)描述了各模式下的驗證流程。

## 若您懷疑有問題

請保留原始資料目錄，並使用另一份副本進行分析。 請透過 [安全政策](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)回報受影響的版本、操作及可重現步驟，同時確保帳戶資料與憑證的隱私。
