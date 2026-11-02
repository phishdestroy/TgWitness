# 連線、代理伺服器與資料保護

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/

驗證、自動代理伺服器池、IP 模式、備用策略、外部請求及機密資料儲存。

本文檔說明 TgWitness 0.8.0 的運作方式及其限制。驗證、 來源存取、網路連線及擷取完整性均為獨立的狀態。 關於登入步驟、檔案格式及多重帳戶，請先參閱「 [帳戶與會話格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/)」；關於事件政策及重新啟動 行為，請參閱[「資料擷取運作方式」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/)。

## 引導式連線設定

在 **Connection** 中，管理員可選擇 **此帳戶**、**帳戶 群組** 或 **所有帳戶**，然後選取路徑。**檢視選項** 會列出 受影響的帳戶。**準備與檢查** 會測試建議的路徑，同時不變更 已儲存的路徑。**套用已檢查的連線** 會再次檢查，若 必要則暫停監測，儲存路徑並恢復已執行的監測。 它絕不會在先前處於閒置狀態的帳戶中啟動資料蒐集。歷史記錄下載仍會 保持暫停狀態，並可另行恢復。切換前請先暫停正在進行的匯出作業。

群組變更預設會讓帳戶保留其原有路徑。請僅在預覽清單中顯示您預期的變更時， 才取消勾選該選項。 應用程式會分別回報 每個帳戶的結果；這並非橫跨資料庫的「全有或全無」式交易。若 切換失敗，該帳戶將恢復至先前設定。若無法恢復，系統會 明確顯示此狀況。預覽將於十分鐘後過期，且若變更連線 設定或群組成員資格，則需重新檢查。

| 路徑 | TgWitness 所管理的內容 |
| --- | --- |
| 直接 | 來自主機的連線；未偵測到外部主機的 VPN，亦未強制執行相關設定。 |
| VPN | 每個帳戶僅有一個全隧道 WireGuard 設定檔，由本機使用者空間的 SOCKS5 程序執行。不會安裝任何主機介面或驅動程式。 |
| 我的代理伺服器 | SOCKS5、HTTP CONNECT 或 MTProxy 憑證。SOCKS5/HTTP 欄位可填入網址。選取多個帳戶時，將共用此處輸入的代理伺服器。 |
| 公開版 MTProto | 現有池會分配 Telegram 路由。在進階設定中配置獨立且合適的代理伺服器之前，外部請求將被停用。 |
| WARP | 為每個選定的帳戶建立獨立的本地隧道，並將 WARP 註冊資訊及 WireGuard 設定檔儲存於該帳戶的保管庫中。 |

當前路徑檢查使用全新的未經認證的 Telegram 傳輸通道，而非 該帳戶的會話。對於支援 HTTP 的路徑，它還會透過該路徑請求 Cloudflare 的 HTTPS 追蹤，並顯示其回報的出口 IP、國家、WARP 狀態 及檢查時間。 所測得的延遲為Telegram連線建立時間， 而非 ICMP ping 測試。除非追蹤報告顯示 WARP 處於活躍狀態，否則 WARP 準備程序將失敗。 這些檢查旨在驗證連線狀態，而非 擷取訊息的真實性或完整性。僅有本地進程正在執行，並不代表出口檢查成功。

### 可攜式 WARP 與 WireGuard

這是 **非官方 WARP 整合方案**，使用 [wgcf 2.3.1](https://github.com/ViRb3/wgcf/releases/tag/v2.3.1) 以及 [wireproxy 1.1.3](https://github.com/windtf/wireproxy/releases/tag/v1.1.3)。 管理員須在首次下載或進行 WARP 註冊前，明確同意此設定。 這些設定連線會直接連至 GitHub 和 Cloudflare，並 洩露該裝置的 IP 位址。一般帳戶的流量會維持原有路由，直到 應用程式啟動為止。Cloudflare 會選擇出口位址及國家；不同的隧道 可以共用同一個出口位址。此功能不提供國家選擇、定期 IP 輪替以及全主機範圍的 VPN 殺手開關。

支援的輔助程式下載版本：Linux 和 macOS x86-64/ARM64，以及 Windows x86-64。 會將建構產出與審查來源碼中捆綁的 SHA-256 雜湊值進行比對， 且在啟動前會再次檢查快取中的可執行檔。 任何輔助程式均不會被加入 PATH 環境變數、安裝為系統服務，亦不會配置公開監聽器。所有檔案皆存放 於工作區的 `portable-routes/` 目錄中，並以加密金庫條目形式儲存。 迴路 SOCKS5 監聽器需使用獨立生成的憑證。

私人設定檔和 WARP 帳戶憑證會透過現有的 工作區金庫進行加密。執行期間，輔助程式需要一份僅限擁有者存取的明文設定檔； 在正常停止時，該檔案會被移除。若主機發生當機，此檔案可能會殘留於 僅限擁有者存取的資料資料夾中。此機制不會加密磁碟，亦無法防止 系統管理員存取。 若面板的父管道 消失，監督程式將關閉隧道。失敗的隧道絕不會啟用直接備援。重新啟動面板 將恢復選定的隧道；啟動失敗時，系統會在限定延遲後重新嘗試。**停止 隧道** 亦會暫停監測並維持停止狀態。**啟動隧道** 啟動隧道；準備就緒時請另行恢復監測。

上傳的 WireGuard 設定檔必須包含一個介面（Interface）和一個對等端（Peer）、完整的 IPv4 及 IPv6 路由，且不得包含鉤子（hooks）、包含（includes）、環境變數替換或額外的 監聽器（listeners）。公開端點位址會在啟動前進行解析並固定。 請使用外部 VPN 或 SOCKS5 閘道，以支援 OpenVPN/IPsec 及私有端點。

合成檢查項目為 `python tools/check_guided_connection.py` 和 `python tools/check_guided_connection_browser.py`。可選的 `python tools/check_portable_routes_runtime.py` 會下載經過驗證的輔助程式，並 透過迴路測試裝置，測試其實際的本地進程生命週期。此操作 不會註冊 Cloudflare 裝置，亦不會使用 Telegram 帳戶。

## 驗證方法

**API ID 和 API 雜湊值用於識別應用程式；它們並不能取代帳戶登入。** 在 TgWitness 中，這些資訊為選用項目。優先順序如下：首先是表單中輸入的一組值，其次是來自 匯入帳戶 JSON 檔案的一組值，接著是儲存於工作區的一組值，最後是內建的 50 組 公開配對組，當 Telegram 拒絕某組時，系統會以隨機順序嘗試並自動輪替。僅 Telegram Desktop 配對組 (2040) 會隨附相應的 Telegram Desktop 客戶端描述一併傳送。 您可將從 [my.telegram.org](https://my.telegram.org) 的 API 開發工具取得的專屬配對組用於所有帳戶；每個帳戶仍保有各自的授權。

| 方法 | 要求 | TgWitness 支援 |
| --- | --- | --- |
| 手機號碼、代碼、可選的雙因素驗證 | 帳戶存取；API 配對為選用項目 | 面板登入 |
| 授權金鑰 HEX + DC ID | 完整的 512 字元金鑰及 DC 1–5 | 「直接**授權金鑰」**分頁；在儲存授權前，會檢查可選的用戶 ID |
| Telethon StringSession | 有效的會話字串 | 面板登入 |
| Telethon SQLite `.session` | 封閉式、一致的文案 | 可直接從面板匯入模式 7/8；可選的離線命令列介面 (CLI) |
| Pyrogram SQLite `.session` | 已關閉的生產環境使用者會話 | 直接匯入模式 2/3 |
| Telegram 桌面版 TData ZIP | 一個現代帳戶；若設有保護，則需輸入本地密碼 | 內存轉換，並包含校驗和／解密檢查 |
| 帳戶 JSON | 支援的 API/會話/金鑰欄位 | 僅憑元資料即可填入 API 憑證；仍需透過會話/金鑰或手機/QR 碼進行登入 |
| QR 碼登入 | 來自授權 Telegram 應用程式的確認 | 本地 QR 碼生成、過期/重試機制，以及可選用的雙因素驗證 (2FA) |
| TDLib / Pyrogram StringSession | 其他特定於資料庫的格式 | 不支援 |
| 機器人代幣 | 一個具備獨立存取／更新模型的機器人 | 此資料蒐集者未使用此工具 |

Telegram 採用代碼傳送方式；簡訊傳送無法保證成功。API 雜湊值無法修復 已被撤銷的連線，亦無法取代遺忘的雙因素驗證 (2FA) 密碼。TgWitness 不會將 登入代碼或 Telegram 雙因素驗證 (2FA) 密碼儲存至磁碟。

若為私人來源，該帳號必須已具備存取權限。群組使用者名稱 並非必要。透過代理或會話匯入，既不會授予成員資格，也不會授予管理員 權限。目前的成員資格並不能保證能存取加入群組前的歷史紀錄。

## 匯入 Telethon 會話檔案

Telethon SQLite、Pyrogram SQLite 以及 Telegram Desktop TData 採用不同的格式。 此面板會偵測並轉換受支援的結構；重新命名檔案並不 屬於轉換範疇。請在「**檔案**」選項中選取一個會話及其對應的 JSON 檔案，然後按下**「連線帳戶」**。最多可接受四個符合條件的檔案， 總大小不得超過 8 MiB。 有關 TData/JSON 的詳細資訊，請參閱[格式限制](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/)。 不提供密碼恢復功能。透過手機/雙因素驗證 (2FA) 或 QR 碼登入將建立獨立的授權。

僅限 Telethon 的可選命令列路徑仍可使用：

1. 請停止使用原始連線的客戶端，並建立一份一致的副本。該 轉換器會拒絕處理 WAL/日誌未完成的檔案。請正確關閉原始 客戶端，而非刪除這些檔案以繞過檢查。
2. 在 TgWitness 環境中，執行：

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. 在「**新增帳戶」→「檔案**」下，載入結果或 貼上其字串，然後繼續。
2. 請確認顯示的數字帳號 ID，選擇來源並開始監測。

此轉換器以唯讀模式開啟 SQLite，不會執行任何資料結構升級或網路請求， 也不會輸出該會話內容。它會檢查資料結構版本、資料表類型、單一 會話列、IP/埠/資料中心以及金鑰長度。命令列介面 (CLI) 輸入限制為 64 MiB；StringSession 文字限制為 4 KiB。 面板轉換會將檔案上傳至已驗證的 TgWitness 伺服器，在記憶體中進行處理，並將標準化的憑證傳回該 瀏覽器，且不會儲存上傳的原始檔案。若使用遠端伺服器，請採用 HTTPS。

**轉換後的檔案為未加密的帳戶存取密鑰。** 請將其存放在受保護的 儲存空間中，切勿將其提交至版本控制系統或傳送給第三方轉換服務。TgWitness 會將授權會話儲存於其加密金庫中。複製會話並不會 建立獨立的授權：請勿同時執行使用克隆授權金鑰的 客戶端，並假設其能獨立接收更新。

轉換操作僅傳遞授權，而非原始訊息、實體快取或 持久性更新游標。此操作不會解決跨程序重啟時的更新復原問題。

## MTProto、Telethon 及代理伺服器

MTProto 是 Telegram 的通訊協定。Telethon 是 TgWitness 所使用的 Python 客戶端函式庫。 MTProxy 是一款 Telegram 傳輸代理伺服器；SOCKS5 和 HTTP CONNECT 提供一般性的 隧道。上述方式均無法取代帳戶驗證。

請在登入前，前往「**帳戶**」**→「設定」→「連線設定」→「變更連線路徑**」，為每個工作區儲存路徑。 新建立的工作區預設為**「自動 MTProxy」模式，**並採用具備「隱藏 IP」功能的**公開清單**。 現有工作區若曾明確使用「直接連線」模式，將保留允許此模式的設定。

## IP 模式

路由決定連線方式。IP 模式則決定伺服器位址 何時可能被曝光。這些控制功能不會安裝 VPN，也不會將所有裝置流量進行路由。

| 模式 | Telegram | 外部請求 |
| --- | --- | --- |
| 隱藏 IP (`hide`) | 請使用代理伺服器；若均無法連線，請稍候。無直接備用方案。 | 需使用 SOCKS5/HTTP；若未透過適用代理伺服器，將拒絕請求。 |
| 允許備用連結 (`fallback`) | 自動 MTProxy 可能會在設定的延遲時間過後使用 Direct 連線，隨後再切回正常運作的代理伺服器。 | 建議使用已設定的外部代理伺服器或該帳戶的 SOCKS5/HTTP 路由；否則允許使用「直接連線」。 |
| Tunnel / VPN (`tunnel`) | 允許使用直連路徑，並可立即自動切換至備用池。 | 若未配置任何適用的代理伺服器，則允許直接連線。 |

隧道／VPN 模式假設您會另行管理該網路。若無運作中的 隧道，目標端將能看見伺服器本身的位址。請根據 您的實際網路環境選擇模式，而非僅依據選項名稱。

### 選擇路徑

| 路徑 | 設定 | 分隔線 |
| --- | --- | --- |
| 自動 MTProxy | 內建清單或運算子目錄 | 維持一條可運作的 Telegram 路徑；直接備用方案取決於 IP 模式 |
| 直接 | 隧道／VPN 模式 | Telethon 使用主機的網路路由 |
| SOCKS5 | 主機、埠號、可選的使用者名稱／密碼 | python-socks，已啟用遠端目標 DNS 功能 |
| HTTP CONNECT | 主機、埠號、可選的使用者名稱／密碼 | 僅支援純 HTTP CONNECT；尚未實作與代理伺服器本身的 TLS 連線 |
| MTProxy | 主機、埠號、密鑰 | 實驗性 Telethon 傳輸格式；32 位元十六進位數字，或 `dd` + 32 位元十六進位數字 |

偽 TLS `ee` 密鑰將被拒絕。Telethon 1.45 的正規化功能可移除前綴 與網域，但並未實作偽 TLS 功能。請貼上 `tg://proxy?server=…&port=…&secret=…` 或 `https://t.me/proxy?server=…&port=…&secret=…`，並選擇「**從連結填入欄位**」。 此操作會在不建立連線或儲存的情況下驗證並填入欄位；請另行檢視並儲存 路由。手動填寫欄位仍可使用。請參閱 [Telegram 代理連結](https://core.telegram.org/api/links#proxy-links)。

### 由您的安裝環境提供的公開代理伺服器

內建清單整合了四個來源： [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto)、 [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro)、 [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) 以及 [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector)。 捆綁的快照包含端點資訊、來源歸屬及下載日期。 供應商名單並不代表該代理伺服器運作正常，亦不保證能傳遞每項 Telegram 更新。

**MTProxy 會自動檢查** Telegram 的傳輸連線狀態，維持一個可運作的代理伺服器， 並在連線失敗時切換至另一個。當有足夠 可運作的代理伺服器時，工作區會優先選用不同的代理伺服器；無法保證會使用唯一的出口位址。 失敗的代理伺服器 會暫停一段時間後再次嘗試。若無任何代理伺服器可用，則由 IP 模式決定 是否必須等待，或可改用直接連線。更換代理伺服器不會變更帳戶 或刪除其日誌。路由選擇與變更皆記錄於簽名日誌中。

當自動路由處於啟用狀態時，清單預設每小時刷新一次，傳輸檢查則 每十分鐘執行一次。這些間隔時間均可自行設定。**更新公開清單** 會觸發刷新；僅瀏覽清單並不會變更已儲存的手動路由。

每個資料源的回應限制為 1 MiB，請求超時為 8 秒， 整體下載時限為 20 秒；重定向 將被拒絕。每個來源最多保留 64 筆相容的條目，並進行去重處理。 解析器支援十六進位數、base64url 密鑰以及 JSON 資料源。 偽造的 TLS `ee`、無效連結、私有／保留的 IP 字面量以及本機主機名稱將被 跳過。主機名稱會在使用前進行解析與檢查，且所選的 IP 地址將被 固定用於該連線。自動重新取得會再次解析主機名稱；若要再次解析，請重新套用 手動輸入的項目。

若饋送回應失敗、為空或不相容，系統將保留先前的來源快照。 更新操作具有原子性與序列化特性，且每分鐘每個工作區僅限嘗試一次。 成功的傳輸探測僅代表連線已建立，並不代表匿名性或擷取完整性。

**Telegram 流量與 HTTPS 請求使用不同的路由。**清單下載會使用 獨立的 HTTPS 連線，並透過提供的外部請求路由進行。 `TGWITNESS_PROXY_FEED_PROXY` 會明確地以 HTTP/SOCKS5 代理伺服器覆寫該路由； 兩種 Compose 版本的收集器皆會轉發該路由。背景池會跟隨主要工作區。 不會將任何 Telegram 會話、API 憑證、控制面板代幣或機器人代幣傳送給資料來源提供者。 提供者名稱、快照日期及下載路徑會顯示於**「清單來源」**欄位下。

MTProxy 僅傳輸 Telegram 流量。工作區的 HTTP 操作（例如時間戳記、 通知、站外副本及來源檢查）在 已設定的情況下，會使用獨立的 SOCKS5/HTTP 代理伺服器， 隨後則使用該帳戶的 SOCKS5/HTTP 路由。若未設定上述任一項，Hide IP 將拒絕 該請求；其他模式則允許直接連線。 外部請求可被停用。經明確 設定的資訊源下載代理仍屬操作員可獨立覆寫的項目。 獨立的見證服務則維持其專屬路由。

透過 SOCKS5 或 HTTP 代理伺服器發送的僅限公開外部 HTTP 請求，會透過 同一代理伺服器，使用 Cloudflare DNS over HTTPS `https://1.1.1.1/dns-query` 解析 目標位址。僅主機名稱及 A/AAAA 查詢類型會傳送至解析器； 服務 URL、憑證及通知內容均不包含在內。 TLS 會驗證 解析器憑證以確認其 IP 位址。系統會檢查兩種位址家族， 若收到任何私有、迴圈、鏈路本位或保留的回應，則會拒絕該請求。 連線會使用經驗證的數值位址，同時保留服務原始的 HTTP Host 及 TLS 憑證名稱。 通知 HTTP 轉發與 CONNECT 請求均採用相同的目標檢查機制。若 DNS 查詢失敗，且無 本地目標 DNS 或直接備用方案，則會中止該請求。成功的回應會依 代理路由分別儲存在記憶體中，最長 30 秒且不超過其 DNS TTL； 快取上限為 128 筆條目。 代理主機名稱本身可使用本機 DNS。 SOCKS 和 CONNECT 失敗時，可在傳送 服務請求正文之前嘗試另一個經過驗證的位址。純 HTTP 轉發會在請求失敗時回報錯誤， 而不會自動透過另一個位址重傳其正文。

對於由營運商管理的私有服務，現有的伺服器環境設定 `TGWITNESS_ALLOW_PRIVATE_DESTINATIONS=1` 可允許私有目的地，並維持 代理端的主機名稱解析。此設定無法透過控制面板啟用。僅限公開 模式會在查詢公開解析器之前拒絕 `.onion` 目的地；Tor 洋蔥 服務需要明確的私有目的地設定以及合適的代理。 此 DNS 行為適用於外部 HTTP 操作，不適用於 Telegram 的傳輸層。 Cloudflare 已針對 [JSON DNS 端點](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/)提供相關文件說明。

****自動池參數**** 在 **參數 → 自動 MTProxy** 下，設定失敗閾值、冷卻時間、 預定輪替、代理伺服器共享及允許的備用延遲。 | 控制項 | 預設值 | | --- | --- | | 替換前斷線次數 | 10 分鐘內 3 次 | | 每次連線嘗試的代理伺服器嘗試次數 | 3 | | 失敗後的首次／最長休息時間 | 10 分鐘／6 小時 | | 預定輪替 | 已停用；失敗時切換 | | 每個代理的帳戶數 | 0：優先使用獨立條目，必要時共享。設定為 1 則會等待專用條目。 | | 允許直接回退前的延遲 | 10 分鐘；Hide IP 仍拒絕直接連線 | | 資訊源刷新／傳輸檢查 | 60 / 10 分鐘；主工作區的設定值適用於共用池 | 不同的代理伺服器並不保證會產生不同的出口位址。這些設定不會 覆寫 Telegram 的限制，亦無法證明匿名性。

若要將公開清單替換為您自己的營運商目錄，請配置以下覆寫設定。 此設定將完全停用外部訂閱功能，即使其 `proxies` 陣列為空時亦然。

將[空目錄](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) 複製到 `proxy-config/proxies.json` ，並新增您已部署的公開端點：

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

必須替換範例值。最多可接受 32 筆不同的條目。 經驗證的清單會回傳標籤／主機／埠號，且不包含共享密鑰；選取其中一項 將把其憑證儲存至工作區金庫中。在進行 明確的傳輸測試之前，可用性尚未經過測試。若目錄格式不正確，則可進行手動設定。

原生啟動：將 `TGWITNESS_PROXY_CATALOG` 設定為本機 JSON 路徑。Docker：

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

該覆蓋層以唯讀模式掛載 `proxy-config`；檔案必須可被容器 UID 10001 讀取。 該目錄不包含在 Git、Docker 建置環境及原始碼存檔中。此 目錄用於配置收集帳戶；[witness 機器人](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/)使用其自身的 HTTP/SOCKS5 路由，而非 MTProxy。

直接備用方案受上述 IP 模式規範。變更路徑前，請先 暫停監測。儲存設定會斷開舊客戶端連線並取消未完成的登入；新 客戶端將使用已儲存的路徑。該帳戶的日誌／會話綁定關係將維持不變。 設定會取代先前路徑：編輯時請重新輸入代理伺服器憑證。

憑證採用 `network.enc` 加密。API 不會回傳使用者名稱、 密碼或機密金鑰。簽名紀錄包含路由類型及是否包含憑證， 但不包含端點與機密金鑰。操作者可在控制面板中查看端點。 機密欄位會在儲存、鎖定或切換工作區後清空。

「**測試 Telegram 連線**」功能（登入前亦可使用），會透過該路徑開啟並關閉一個臨時 且未經授權的 Telegram 連線。此功能不會聯繫任何 IP 檢查 網站。測試成功僅表示傳輸連線已建立，並不代表群組存取權限、訊息 完整傳送或匿名性。

此代理適用於 Telegram 客戶端的連線，包括 Telegram 數據中心（DC）的媒體 下載。瀏覽器、pip、SSH 以及手動調用的 TSA 工具則有獨立的路由。 代理主機名稱可於本地解析。`rdns` 會影響目標主機名稱； Telegram 通常會提供數據中心的數值 IP 位址。

SOCKS5 和純 HTTP CONNECT 本身並不會加密代理憑證或 客戶端至代理的隧道。MTProto 會另行保護 Telegram 流量。 在不可信的網路環境中，請使用 適當的安全通道連線至代理伺服器。私人群組 屬於雲端聊天；MTProto 並不會將其轉變為端對端加密的「秘密聊天」。

## 加密與簽名

| 層級 | 已實作 | 操作員責任 |
| --- | --- | --- |
| Telegram 通訊流量 | Telethon MTProto | 平台可信度、傳輸路徑與可用性 |
| 網頁控制面板 | 承載者代幣、迴路預設值、請求限制 | 透過 HTTPS 或 SSH 隧道進行遠端存取 |
| 秘密 | Fernet 用於管理 API 憑證、會話、代理伺服器憑證及簽名私鑰 | 保護解密金鑰與運行主機 |
| 金庫金鑰 | 新安裝時使用本機金鑰或外部主金鑰 | 獨立的受保護儲存空間與金鑰備份 |
| 訊息與附件 | 明文應用程式儲存 | 加密磁碟／磁碟區 |
| ZIP/JSONL/CSV/HTML | 完整性檢查，無內容加密 | 保護匯出副本與傳輸內容 |
| 來源與時間 | 簽名日誌、流程收據、RFC 3161 工具 | 可信密鑰、獨立檢查點／TSA 及保管程序 |

「帳戶」中的**儲存保護功能**會顯示這些狀態。面板憑證是一種 存取密鑰，而非加密密碼。它授予管理員存取權限； [已發行的憑證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/)可限定於特定帳戶和聊天室。工作區共享 主進程，並非獨立的租戶。

一個明確啟動且隔離的合成示範環境，可透過直接 迴路連接自動開啟。此功能採用獨立的進程生命週期機制；既不會 洩露已設定的面板憑證，也不會授予存取真實工作區的權限。遠端、 代理或跨來源的請求均無法取得或使用此自動進入功能。 此便利功能並不會消除針對真實帳戶資料的驗證邊界。

BitLocker、LUKS、FileVault 或受管加密卷宗皆可在 各自的威脅模型下保護儲存裝置。 已解鎖且正在運行的機器之管理員 仍可讀取資料。在儲存規劃中，應納入 SQLite WAL/SHM、媒體檔案、臨時匯出檔案、交換檔、備份 以及瀏覽器下載檔案。Docker 卷宗並非僅因 其為卷宗而自動加密。TgWitness 未實作 SQLCipher 或物件加密功能。

## 外部主金鑰

若要進行新安裝，請將主金鑰放置於資料目錄之外。 此操作不會自動遷移現有的本機金鑰保管庫。請準備一個 僅限服務身分存取的金鑰目錄，然後執行：

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell，使用已安裝的專案環境：

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

在 Docker 中，請將檔案以唯讀方式掛載至 `/data` 之外的目錄（例如 `/run/secrets/tgwitness-master.key`），並將環境變數設定為該路徑。 該服務的 UID 必須具備讀取權限。請透過 環境變數／設定檔傳遞路徑，而非金鑰位元組。

每個工作區都會獲得一個隨機的公開鹽值，以及透過 HKDF-SHA256 衍生的專屬 Fernet 金鑰。`vault.external.json` 僅儲存衍生元數據，而非主金鑰。 若金鑰遺失或錯誤，系統將無法啟動，且不會在後台自動替換金鑰。請同時保留 鹽值元數據與主金鑰，以備復原之用。

所有工作區均源自同一主金鑰；若主金鑰遭洩露，將影響整個 安裝環境。正在執行的程序可解密機密資料。此工具並非 HSM 或 密碼 KDF。不接受以任意人為設定的密碼取代隨機金鑰。

在刻意規劃的遷移方案 實施並驗證完成之前，請保留現有安裝環境中的現有金鑰。刪除 `vault.key` 或更換主金鑰可能會導致 無法存取會話／簽署金鑰。請將加密備份與金鑰分開存放，並 在隔離的實例中測試還原功能。

## 資料來源與驗證範圍

審閱日期：2026年10月26日：

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0：SQLiteSession、StringSession、`Connection._proxy_connect`、 `TcpMTProxy.normalize_secret` 及下載方法。

本地測試涵蓋迴路 SOCKS5/HTTP CONNECT 測試案例、模擬的 SQLite 會話、 路由隔離、機密資料排除以及缺失金鑰時的拒絕機制。這些測試並未建立 真實的 Telegram/代理伺服器互通性，亦未模擬 MTProxy 的實際運作行為。請參閱 [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/) 及 [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)。
