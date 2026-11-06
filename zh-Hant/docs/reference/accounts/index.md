# Telegram · 帳戶與會話格式

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/

可透過手機、QR 碼或授權金鑰登入，匯入 Telethon、Pyrogram 或 Telegram Desktop 的會話紀錄，並同時管理多個帳戶。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [開始使用](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/quickstart/)

![開始使用](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

TgWitness 透過 MTProto 協議，使用 Telethon 以 Telegram 用戶帳戶（而非機器人）身分登入。每個帳戶皆位於獨立的工作區中（在 API 和命令列工具中稱為「工作區」），並擁有專屬的會話、來源、日誌及簽名金鑰。

會話檔案、會話字串及認證金鑰均屬**帳戶授權憑證**：凡 持有其中任何一項者，皆可代表該帳戶進行操作。這些資料不包含訊息歷史紀錄。

> [!警告] **請勿使用任何您無法承受損失的資料。**我們強烈建議不要連結 個人帳戶或其他重要帳戶，也不要使用您重視的帳戶來建立 API ID 或 API 雜湊值。 這並非因為 TgWitness 未經測試：Telegram 會以不可預測的方式限制並 永久封禁帳號——只要其認為請求量 過高，無論使用何種客戶端或出於何種目的，且未提供充分的文件說明。許多封禁 措施皆無法撤銷。 請使用專用帳號。測試能否順利進行取決於 Telegram，而非 軟體本身，且無法保證後續運作無虞。

- [一覽](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#at-a-glance)
- [開始之前：API ID 與 API 雜湊值](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [電話號碼](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#phone-number) · [QR 碼](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#qr-code) · [授權金鑰 + DC 識別碼](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#auth-key--dc-id)
- [帳戶檔案](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#pyrogram-session) · [會話 + JSON 對](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#telethon-stringsession) · [帳戶 JSON](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#account-json)
- [釐清您所擁有的內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#identify-what-you-have) · [不支援的格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#unsupported-formats)
- [多個帳戶](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#multiple-accounts) · [確保帳戶檔案安全](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#keeping-account-files-safe) · [疑難排解](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#troubleshooting)

## 一覽

| 您現有的內容 | 「**新增帳戶**」分頁 | 您還需要 |
| --- | --- | --- |
| 電話號碼及其登入代碼的存取權限 | **電話** | 若已啟用，則為雙因素驗證 (2FA) 密碼 |
| Telegram 已在另一台裝置上開啟 | **QR 碼** | 若已啟用，則為雙因素驗證 (2FA) 密碼 |
| `.session` 檔案（Telethon 或 Pyrogram） | **檔案** | 可選的 JSON 檔案，用於應用程式設定 |
| `.session` + `.json`（名稱相同） | **檔案**（請選取兩者） | 通常沒有其他內容 |
| Telegram 桌面版中的「`tdata`」資料夾 | **檔案**（ZIP 壓縮檔） | 若已設定，則為桌面版本機通行碼 |
| 一場 Telethon StringSession（文字、`.txt`、`.tgwitness-session`） | **檔案** | 無需額外配對的 API |
| 一個附帶會話或認證金鑰的 `.json` | **檔案** | 無需額外配對的 API |
| 一個授權金鑰（512 個十六進位字元）及其 DC 編號 | **授權金鑰** | 可選使用者 ID |

TgWitness 根據檔案**內容**而非檔案名稱來識別檔案。重新命名檔案 絕不會導致其轉換。

## 開始之前：API ID 與 API 雜湊值

您無需建立 Telegram API 應用程式即可登入。當未輸入、 未匯入或工作區中尚未儲存任何密鑰對時，TgWitness 會從其內建的 50 組公開 API 密鑰對池（`tgwitness/api_pool.py`）中選取一組，若為首次 登入則優先選用 Telegram Desktop 的密鑰對，並優先保留已儲存的密鑰對；其餘候選密鑰對則會隨機排序。 若 Telegram 拒絕某組密鑰對 （`API_ID_INVALID`、`API_ID_PUBLISHED_FLOOD`、`UPDATE_APP_TO_LOGIN`），系統將嘗試下一組， 每次登入最多嘗試八組；遭拒絕的密鑰對將被跳過，直至重新啟動。成功登入的密鑰對將 與該帳戶一同儲存，並供該帳戶重複使用。**API ID** 與 **API 雜**湊值用於向 Telegram 識別應用程式；它們 本身並不會授權任何帳戶。

若缺少連線欄位，則使用捆綁的 [opentele2 2.0.0 目錄](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735)中預設的確定性裝置/作業系統組合： 桌面版 `2040`、Android `6`、Android X `21724`、iOS `10840`、macOS `2834` 以及 Web `2496`。 Android 的原始碼建置 ID `4` 亦採用 Android 目錄，此資訊可於 [Telegram Android 的 BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java) 中查證。 Web 預設為 A；若導入 `K` 應用程式版本後綴或 `macos` 語言套件，則選取 K；版本 `0.7.0` 則選取 Webogram。未知應用程式 ID 將維持 Telethon 的主機 預設值。導入的欄位始終具有優先權，包括較舊的應用程式版本及空的 語言套件。目錄絕不會變更 API ID/雜湊值。其版本快照會 經過明確審查，而非於登入時自動擷取。儲存的設定檔在更新後仍保持穩定。

`account.getAuthorizations` 會回報 Telegram 儲存的授權元資料；這 並非每次執行 `initConnection` 時的即時回響。請將其與實際傳送的設定檔進行比對。 連接現有授權並不會驗證其對應的 API 雜湊值： `initConnection` 會傳送 API ID，而雜湊值則用於登入請求。

在進行新手機或 QR 碼授權後，TgWitness 會依序請求設定檔、最近的數據中心、 線上狀態、語言（當語言套件不為空時）、應用程式更新及 服務條款更新，各次請求之間間隔 0.3 至 1.5 秒。 更新狀態 會短暫將帳戶標記為線上狀態。此流程僅在登入完成時執行一次， 不會在匯入資料、重新連線或重新啟動時執行。授權資訊會優先儲存；若請求失敗， 流程將立即中止，不會重試或捨棄登入資料。結果會 記錄為 `account.initialized`，內容為錯誤名稱而非回應正文。 此流程無法保證帳戶不會受到限制。

對於 `tdesktop` ，若未指定 `tz_offset` ，則會使用伺服器的本地 UTC 偏移量，並透過 [opentele2 演算法](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) 四捨五入至 900 秒 （MIT；授權條款見 `tgwitness/client_profiles.LICENSE` ）。此值會在每次 連線時更新，以反映夏令時變更。在所有平台上，已匯入的 `tz_offset` 均具有優先權，且會精確保留（包括零值）。其他 `initConnection.params` 項目則予以保留。 HTTP 登入表單接受檔案匯入所回傳的數值時區； 布林值、小數以及超出支援範圍的偏移量均會被拒絕。

直接、SOCKS5 及 HTTP CONNECT 路由均採用 Telethon 的 `ConnectionTcpObfuscated` （經混淆的簡化版 MTProto）。HTTPS CONNECT 維持與代理伺服器之間的 TLS 連線，並在隧道內使用 相同的混淆傳輸協定。MTProxy 則維持其所需的 隨機化中間傳輸協定與密鑰處理機制。路由切換時亦採用 相同的選項。 混淆處理會改變封包的幀結構；它並不會向 Telegram 隱藏 帳戶或其客戶端元資料，亦不表示能免受限制。

在連線至授權客戶端後，TgWitness 會檢查設定、最近的資料中心、 當前授權狀態、已審核的層級基準、語言、應用程式更新 以及服務條款更新。這些診斷程序會在每個客戶端實例中執行一次， 且在資料蒐集之前進行，並會連同執行時間一併顯示於連線詳細資訊中。 `account.connection_checked`會記錄結果，但不包含會話雜湊、IP 位址、 標記或 API 雜湊。它們絕不會接受條款或安裝更新。若發生 請求失敗或 FloodWait 狀態，後續請求將停止；若結果缺失，則維持未知狀態。 即使跳過網路檢查，本地檢查仍可回報其結果。

FloodWait 診斷資訊會保留失敗的 TL 方法、任何 Takeout/range 封裝器、 伺服器要求的等待時間，以及 `telegram.backoff` 中的有效截止時間。 當請求暫停時，連線詳細資訊會顯示方法與截止時間。 該診斷資訊包含自該客戶端建立以來 各方法的客戶端呼叫計數器；這些計數器會分別統計嵌套的對等節點解析次數，但不會計入封包 或 Telethon 的內部重試次數。當前計數器亦可透過狀態 API 中的 `collector.rpc_activity` 取得。 不包含任何請求參數、使用者名稱、存取 雜湊值或例外訊息。最後的診斷記錄與完整截止時間 在重新啟動後仍會保留。較早且未記錄方法的等待狀態 無法事後歸因。請參閱來源審查的[匯出限制](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md)， 以及「發現」與「歷史資料擷取」之間的區別。

`official_app=True` 或 `False` 是 Telegram 的當前授權標誌。這兩種 值均無法判定該帳號是否受限、受信任或正處於監測狀態。 現有的證據模式 `account.devices` 快照仍保留所有 已登入裝置的歷史紀錄；連線診斷則僅保留當前裝置的描述。

連線前，諮詢性檢查會將 API 平台、語言套件、 裝置／作業系統與應用程式版本格式、行動系統地區設定，以及 Telethon 的實際 架構層，與已審核的目錄基準進行比對。警告訊息會顯示於伺服器 日誌及帳戶狀態元資料中；這些警告絕不會取代匯入的值，也不會變更 架構層。 不同層級僅代表相容性審查訊號，並非證明該 帳號已失效或受限。這些檢查及 `official_app` 並未保證 Telegram 認定該帳號不受限制。已斷開連線的帳號狀態 會使用儲存的個人資料，而非重新生成另一份裝置描述。

若要改用您自己的應用程式（註冊該應用程式的帳戶將面臨風險；請參閱「 [為何需要內建的 API 池？](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)」）：

1. 開啟 [my.telegram.org](https://my.telegram.org) 並使用您擁有的任何電話號碼 登入。驗證碼將發送至 Telegram 應用程式，而非透過簡訊。
2. 選擇 **API 開發工具**。
3. 建立應用程式：任選標題與簡稱（5–32 個字母），平台選「**桌面版**」。 網址與描述欄位可留空。
4. 請複製 **App api_id**（一個數字）和 **App api_hash**（32 個十六進位字元）。

在登入表單下方的面板中，會顯示「**API ID + Hash**」。您可將一組 `api_id:api_hash` 組合貼上至 **API ID** 欄位，系統便會自動填入兩個欄位。同一組組合可 適用於您所有的帳戶。成功登入後，該組合將以加密形式儲存於 該工作區內，且絕不會傳回瀏覽器。

涉及三種不同的憑證：

| 機密 | 開啟 | 存放位置 |
| --- | --- | --- |
| 面板代幣 | TgWitness 網頁控制面板 | 資料目錄中的 `panel-token.txt`，或 `TGWITNESS_TOKEN` |
| API ID + 雜湊值 | 本身並無特殊含義；僅用於識別該應用程式 | 可透過內建配對、匯入設定，或於 my.telegram.org 建立您專屬的應用程式 |
| 帳戶授權 | Telegram 帳號 | 可透過手機／QR 碼登入建立，或作為會話匯入 |

若必須透過代理伺服器連線至 Telegram，請先前往「 **帳戶」→「設定」→「連線設定」→「變更連線路徑**」進行設定。

## 電話號碼

1. 開啟「**帳戶**」頁面，切換至**「電話」**分頁，並以國際格式輸入號碼， 例如 `+44 7700 900123`。空格和連字號會自動移除。
2. 按下「**繼續**」。API ID + Hash 欄位可留空。
3. 請輸入 Telegram 發送的驗證碼（通常發送至 Telegram 應用程式；無法保證會透過簡訊發送）。
4. 若該帳號啟用了兩步驟驗證，請輸入該密碼。此密碼並非控制面板 代幣，亦非裝置通行碼。
5. 登入後請確認顯示的帳號 ID，然後選擇資料來源。

登入代碼與雙因素驗證 (2FA) 密碼絕不會寫入磁碟。

## QR 碼

當該帳號已在手機或另一台電腦上登入時，請使用此功能。

1. 點擊「**QR 碼」**→ **顯示 QR 碼**。API ID + Hash 欄位可留空。
2. 在已登入的裝置上：**設定 → 裝置 → 連結桌面裝置**，掃描條碼 並確認。
3. 若 Telegram 要求，請在 TgWitness 中輸入雙因素驗證 (2FA) 密碼。

此 QR 碼圖像係於本地端產生。QR 碼會過期；請按「**產生另一個 QR 碼」** 以重新嘗試。若鎖定面板、切換工作區或啟動另一組登入程序，將取消 待處理的 QR 碼。

## 授權金鑰 + DC 識別碼

授權金鑰（Auth Key）是每個 Telegram 連線背後 256 位元的原始授權資料，以 **512 個十六進位字元**表示，並附有資料中心編號 **DC 1–5**。

1. 「**Auth key**」分頁。請貼上完整的金鑰；若金鑰中包含「`…`」等縮寫，則無法正常運作。
2. 請選擇隨金鑰一併提供的 DC ID。
3. 可選擇輸入**使用者 ID**。若 Telegram 回報 帳戶不符，TgWitness 將拒絕連線。
4. Press **Connect 帳戶**。

授權金鑰（512 個字元）並非 API 雜湊值（32 個字元）。同一組金鑰亦可 以 JSON 格式匯入，詳見「[帳戶 JSON](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#account-json)」。

## 帳戶檔案

開啟**「新增帳戶」→「檔案」**，並選取最多**四個屬於同一帳戶的檔案**（總計 **8 MiB**），然後按下「**連線帳戶」**。

「**檔案**」、**「授權金鑰」**及「批量匯入」表單會在連線前顯示 「並行會話」警告。預設情況下，匯入的授權將被重複使用。當其金鑰 在此處使用時，請保持原始 客戶端關閉。**檔案**與**授權金鑰**亦提供 「**建立獨立授權**」功能，詳見下文說明。批量匯入仍使用 直接模式。手機及互動式 QR 碼登入會建立獨立的授權。 警告標題在匯入表單中始終可見；當提供檔案或金鑰／會話字串時，其完整說明會 自動展開。閱讀後可將其收起， 以便在手機上仍能正常使用檔案瀏覽器與連線控制項。

- 檔案會在您的 TgWitness 伺服器**記憶體中**進行轉換。上傳的檔案不會被儲存， ZIP 檔案不會解壓縮至磁碟，也不會與任何外部服務進行連線。
- 隨後會將生成的會話記錄與 Telegram 進行比對。若檔案中載明使用者 ID， 則該 ID 必須與 Telegram 回報的帳戶相符。
- 描述不同帳戶或不同 API 憑證的檔案將被拒絕 而非僅選擇其中一個。
- **密碼或會話文字**欄位包含 TData 的本地密碼欄位，此處可貼上 StringSession 並**讀取檔案**，**無需登入**（填寫表單時無需 聯繫 Telegram）。

### 建立獨立的授權機制

請選擇「在連線前**建立獨立授權」**並匯入檔案，或 選用「授權金鑰」。TgWitness 會短暫連線至匯入的「捐贈者」，利用其核准 新客戶端的 QR 登入憑證，並在核准後立即斷開與「捐贈者」的連線。 新客戶端擁有專屬的授權金鑰，以及獨立選定的桌面 設定檔。「捐贈者」提供的 API 憑證與裝置設定檔僅用於 與「捐贈者」的連線。現有的授權不會被登出或撤銷。

**在此步驟中，請務必將捐贈者的原始客戶端完全關閉。**初始 連線仍使用其複製的金鑰，因此此模式無法消除該初始 並行使用的風險。一旦建立新的授權連線，擁有者即可重新開啟 原始客戶端，並獨立使用兩者。互動式 **QR 碼**登入功能可讓 原始客戶端在無需在此處複製或連線其金鑰的情況下，批准此次登入。

若 Telegram 要求雙因素驗證（2FA），此模式會使用選取的 JSON 檔案中的 `twoFA`（若存在）， 否則將要求輸入密碼。若匯入的密碼遭拒，系統將返回密碼輸入表單。 密碼不會被儲存。候選金鑰會以加密形式儲存於 `independent_login.enc` 中，包含資料中心遷移期間的變更。發生 中斷後，請選取相同的來源帳號並選擇此選項，以恢復已儲存的候選金鑰。 工作區仍會為該帳戶保留；即使完成進程失敗，也不會刪除 新的工作區。請保留其資料目錄和金庫金鑰。最終的憑證及 `account.authorized`日誌記錄將包含匯入方法、輸入格式以及 來源 API ID，但不會包含來源金鑰或密碼。

2026年11月5日，一個專用帳戶通過了 Telethon、Pyrogram 及 TData 捐贈者的即時驗證：2 因素驗證（2FA）完成、獨特的新授權金鑰、捐贈者與新客戶端 的並行存取，以及閱讀公開頻道。 Telethon 案例中， 系統亦在密碼輸入步驟中發生中斷後，成功恢復了已儲存的候選帳戶。每個新的 授權皆完成了登入後的六項初始化請求，且其簽署過的 日誌已通過驗證。原始會話在所有四種提供的格式中均保持可用。

Telegram 的 [RPC 錯誤資料庫](https://core.telegram.org/api/errors.json)將 `FRESH_CHANGE_ADMINS_FORBIDDEN` 與變更管理員、`FRESH_CHANGE_PHONE_FORBIDDEN` 與變更電話號碼，以及 `FRESH_RESET_AUTHORISATION_FORBIDDEN` 與 撤銷其他會話、變更其有效期或註冊通行金鑰相關聯。 `SESSION_TOO_FRESH_*` 和 `PASSWORD_TOO_FRESH_*` 涉及所有權轉移以及 收益或禮物提領。這些並非資料擷取操作；新登入並不 意味著全面性的 24 小時讀取禁令。匯出功能可另行返回 `TAKEOUT_INIT_DELAY_*`。TgWitness 會保留伺服器要求的暫停狀態，且不會自動重試 代幣接受或撤銷會話以規避限制。

### Telethon `.session`

|  |  |
| --- | --- |
| 產品簡介 | 由 Telethon 衍生工具所建立的 SQLite 資料庫，例如 `my_account.session` |
| 獲以下機構認可 | 表格 `sessions`（連同 `dc_id`、`server_address`、`port`、`auth_key`）及 `version` = 7 或 8 |
| 要求 | 僅有一筆授權會話記錄；一個封閉且完整的数据庫 |

請先關閉建立該檔案的程式。若其旁邊存在 `my_account.session-journal` 或 `my_account.session-wal`，表示資料庫尚未完成：請正常開啟並 關閉原始客戶端。刪除這些輔助檔案可能會留下損壞的副本。

### Pyrogram `.session`

|  |  |
| --- | --- |
| 產品簡介 | 基於 Pyrogram 的工具所建立的 SQLite 資料庫 |
| 獲以下機構認可 | 表格 `sessions` 包含 `dc_id`、`auth_key`、`test_mode`、`user_id`、`is_bot`；`version` = 2 或 3 |
| 要求 | 生產環境網路中僅允許一個授權**使用者**會話。機器人及測試資料中心（test-DC）的會話將被拒絕 |

登入時，系統會將儲存的用戶 ID 與 Telegram 進行比對。

### 會話 + JSON 對

帳戶資料通常以兩個同名檔案的形式分發，例如 `447700900123.session` 和 `447700900123.json`。請一次選取**兩者**。

- 根據 JSON 資料，TgWitness 使用 `app_id`/`api_id` 及 `app_hash`/`api_hash`，因此您 通常無需手動輸入 API 憑證。
- 連線設定檔使用 `device_model`（別名 `device`）、`system_version` （別名 `sdk`）、`app_version`、`lang_code`、`system_lang_code`（別名 `system_lang_pack`）、 `lang_pack` 以及可選的 `tz_offset`（以秒為單位的 UTC 偏移量，範圍為 -43200 至 50400）。 手動填入的欄位優先於系統生成的預設值及控制面板／瀏覽器的 語言設定。若別名發生衝突，則不予接受。解析後的設定檔將儲存於 加密的工作區憑證中，並在重新啟動後重新使用，其中包含其應用程式版本。
- `phone`、代理伺服器設定及裝置代碼將被**忽略**。`twoFA` 僅在 選取「**建立獨立授權」**時為唯讀；直接匯入則會忽略此項目。
- 若 JSON 缺乏受支援的授權欄位，則僅為元資料。請新增其 會話檔案，或繼續使用手機或 QR 碼登入。若 JSON 包含受支援的會話或 授權金鑰，即可自行完成授權；詳見「[帳戶 JSON](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#account-json)」。

### Telegram 桌面版 (TData)

TData 即是 Telegram Desktop 應用程式（來自 desktop.telegram.org 的跨平台 應用程式）中的 `tdata` 資料夾。

| 系統 | 預設位置：`tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata`（可攜式 Telegram：位於 `Telegram.exe` 旁邊） |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

若要導入此工具：

> **並行會話警告。**直接匯入 TData 會重複使用 Telegram Desktop 的授權 金鑰。請勿同時在 Desktop 和 TgWitness 中使用該金鑰。Telegram 可能會透過 `AUTH_KEY_DUPLICATED` 使授權失效，導致兩份副本在重新登入前皆無法使用。
>
>
>
> 請完全關閉 Desktop（包括其系統托盤進程），並在 TgWitness 使用匯入的會話期間保持該副本關閉。**請直接關閉程式，切勿登出或撤銷會話：** 撤銷會話也會使匯入的副本失效。若您需要同時運行兩個客戶端， 請選擇**「建立獨立授權」**，並在 新登入成功前保持 Desktop 關閉，或透過手機或 QR 碼登入 TgWitness。建議使用 專用帳戶，但這並不能確保複製的金鑰在並行使用時是安全的。
>
>
>
> 此規則同樣適用於匯入的 `.session` 檔案、StringSession 文字及 Auth Key HEX。 其他擁有獨立建立之授權的用戶仍可保持登入狀態。 請參閱 [Telegram 的 AUTH_KEY_DUPLICATED 文件](https://core.telegram.org/api/errors#406-not-acceptable)。

1. 完全退出 Telegram Desktop。
2. 請從 `tdata` 中擷取僅包含以下兩項內容的 ZIP 檔案：

   - `key_datas`
   - 其旁邊以 `s` 結尾的 16 字元檔案，通常為 `D877F783D5D3EF8Cs`

   將整個資料夾連同其媒體快取一併壓縮為 ZIP 檔時，通常會超過限制 （512 筆記錄，解壓縮後 32 MiB）。 3. 在**「檔案**」中選取 ZIP 檔。若 Telegram Desktop 設有**本機密碼**，請先在 **「密碼」或「會話文字」**欄位中輸入該密碼。此並非雙因素驗證 (2FA) 密碼。

支援功能：每個存檔僅限一個帳戶、現代化的 `key_datas`/`key_data0`/`key_data1` 儲存技術， 以及本機密碼。不支援功能：包含多個已登入帳戶的資料夾、較舊的桌面版 介面佈局、受密碼保護的 ZIP 檔案，以及獨立的原生 macOS 應用程式「Telegram for macOS」。

### Telethon StringSession

單行文字，通常以 `1` 開頭，長度約 350 個字元。請將其 載入為 `.txt` 或 `.tgwitness-session` 檔案（最大 4 KiB），或貼至 **「密碼」或「會話文字」**欄位下方。僅接受 Telethon 字串；Pyrogram 和 TDLib 字串採用不同格式。

### 帳戶 JSON

一個 JSON 物件，大小最多 **64 KiB**，存於副檔名為 **`.json`** 的檔案中。

| 欄位（別名） | 含義 |
| --- | --- |
| `api_id` (`app_id`) | 應用程式 ID，一個正整數 |
| `api_hash` (`app_hash`) | 應用程式雜湊值，32 個十六進位字元 |
| `string_session`（`session_string`、`session_str`；舊版 `session`） | Telethon StringSession 文字內容，並非檔案名稱 |
| `auth_key` (`auth_key_hex`) + `dc_id` | 完整的 512 字元授權金鑰及 DC 1–5 |
| `user_id` (`id`) | 可選；在儲存授權前會與 Telegram 進行比對 |
| `device_model` (`device`) | 連線裝置說明 |
| `system_version` (`sdk`) | 連線作業系統版本 |
| `app_version` | 發送至 Telegram 的應用程式版本 |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | 客戶端語言、系統語言及客戶端語言套件；允許使用空的 `lang_pack` |
| `tz_offset` | 可選的 UTC 偏移量（以秒為單位），透過 `initConnection.params` 傳送；格式為整數或十進位整數字串 |

若同時存在別名與主名稱，兩者必須一致。明確的 Telethon 會話欄位優先於其他格式的通用 `session` 二進位資料。若 兩者均包含可識別的 Telethon 會話，則必須描述相同的授權。 若無明確欄位，`session` 必須為有效的 Telethon StringSession。範例：

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

第一個範例僅需填入 API 憑證；您可透過手機或 QR 碼登入，或新增一個會話 檔案。系統不接受批次清單（帳戶的 JSON 陣列）。

## 釐清您所擁有的內容

| 您會看到 | 它是一項 | 使用說明 |
| --- | --- | --- |
| `*.session`；在文字編輯器中開啟時，頂端顯示 `SQLite format 3` | Telethon 或 Pyrogram SQLite | **檔案**（自動偵測） |
| 一個名為 `tdata` 的資料夾，其中包含 `key_datas` | Telegram 桌面版 TData | 將兩個檔案壓縮為 ZIP 檔，然後前往「**檔案」** |
| 以 `1` 開頭的一行文字，約 350 個字元 | Telethon StringSession | **檔案** |
| `*.json` 搭配 `app_id`/`app_hash` | 相關元資料 | **檔案**及其對應的會話 |
| `*.json` 搭配 `auth_key` 或 `string_session` | 帳戶 JSON | **檔案** |
| 512 個字元 `0-9a-f` | 授權金鑰 | **授權金鑰** |
| 32 個字元 `0-9a-f` | API 雜湊值 | **API 識別碼 + 雜湊值** |
| 來自 TDLib 應用程式的 `td.binlog` 或 `db.sqlite` | TDLib 儲存 | 不支援 |
| `123456789:AA…` | 機器人代幣 | 不支援 |

## 不支援的格式

| 格式 | 替代版本 |
| --- | --- |
| TDLib 儲存 (`td.binlog`) 及 TDLib 匯出功能 | 透過手機或 QR 碼登入 |
| Pyrogram 會話**字串** | 請使用 Pyrogram `.session` 檔案，或透過手機/QR 碼 |
| TData 附帶多個已登入的帳戶 | 請在 Telegram Desktop 中登出其他帳戶，或使用各帳戶專屬的會話檔案 |
| 機器人代幣 | 不支援：TgWitness 僅以使用者帳戶身分進行監測 |
| 包含多個帳戶的 CSV/JSON 清單 | 透過**帳戶 → 匯入帳戶**匯入受支援的工作階段檔案，或在個別的工作區中透過電話號碼／QR 碼登入 |
| Test-DC 或 機器人會話 | 請使用正式運作的用戶帳戶 |

## 多個帳戶

請按下帳戶選擇器旁的 **+**，或開啟 **帳戶 → 設定 → 連線設定 → 工作區**，輸入標籤並 登入。

- 可建立任意數量的工作區，包含主工作區在內。每個工作區皆擁有獨立的會話、代理 路由、來源、擷取政策、日誌、簽名金鑰、檢查點及匯出設定。
- 切換顯示中的工作區並不會暫停其他工作區的運作。
- 日誌會與建立它的帳戶綁定。若以其他 帳戶登入，則需建立另一個工作區，且一個帳戶無法被指派至兩個 工作區。
- 主面板中的「代幣」功能可控制所有工作區。[所發出的存取權限](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/)可將其他使用者限制在選定的帳戶和聊天室中，並可設定獨立的權限與會話限制。
- **帳戶會**重新命名一個工作區，並刪除已新增的工作區，連同其會話、日誌、 來源及簽名金鑰一併刪除。主工作區無法從控制面板中刪除。

### 批次匯入和帳戶群組

請使用「**帳戶」→「匯入帳戶」**來新增多個帳戶，根據檔案基名配對檔案 並查看每個登入結果。每個帳戶都會擁有專屬的工作區。

群組可將相關帳戶彙整在一起，同時不會合併其會話、金鑰或 證據。在「**帳戶」**中**開啟「群組」**將導向其頁面： `/groups/<id>`:

- **帳戶:**每位成員的連線路徑、觀察記錄及最後一則訊息，並附有 「**全部**啟動」與「**全部暫停」功能**。
- **需要注意:**已登出、無法使用，或存在 連線、匯入、來源或媒體問題的帳戶；每個名稱皆可導向其對應的卡片。
- **多個帳戶可查看的聊天內容包含：** 共享來源、正在監看這些來源的帳戶，以及 可用工作區監看期間（最長七天）內的中斷情況。**使用 N 個帳戶進行匯出時，** 系統會將頻道或超級群組的匯出內容分配至各帳戶，並對單一存檔進行簽署。
- **匯出群組:**包含一個 ZIP，其中每個帳戶的簽名匯出檔位於 `accounts/` ，並 `manifest.json` 列出其SHA-256與金鑰指紋，並由主 工作區在 `manifest.signature.json`。請使用 `python -m tgwitness.verify` 並使用該帳戶的可信指紋，分別驗證每個帳戶的存檔。

成員共享群組的設定；每個帳號可保留其自身的設定值。 請參閱「[共享設定](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/settings/#account-groups)」、 [「匯入與群組指南」](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) 以及 [MTProxy 資料池儀表板](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources)。

## 登出

「**帳戶 → 登出 Telegram**（暫停監測）」會要求 Telegram 終止該 連線，因此該連線也會從帳戶的「**設定 → 裝置**」中消失，並將該 連線從工作區金庫中移除。日誌、來源、設定和簽名金鑰仍會保留，且 日誌會記錄此次登出操作。 該工作區仍歸屬於其帳戶：僅有該 帳戶可再次連線至該工作區。若 Telegram 未回應，該連線仍會在此處被移除 ，且控制面板會顯示此訊息；請在 Telegram 的「**設定」→「裝置」**中結束該連線。

## 確保帳戶檔案安全

- 請將每個 `.session`、TData ZIP、StringSession、Auth Key 及帳戶 JSON 視同 密碼般嚴加保護。TgWitness 會將匯入的授權資訊儲存於其加密金庫中；您可 於事後刪除原始檔案。
- 請勿同時在兩個程式中執行相同的授權。Telegram 可能會撤銷該授權 (`AUTH_KEY_DUPLICATED`)，屆時兩個程式都將無法運作。
- 已過期或遭撤銷的連線無法透過轉換恢復。請重新登入。

## 疑難排解

| 訊息或徵兆 | 操作指南 |
| --- | --- |
| *無法讀取此會話。請關閉其原始客戶端……* | SQLite 檔案目前處於開啟狀態或尚未完成（`-journal`/`-wal` 輔助檔案）。請先正常關閉原始程式，然後重新複製該檔案。 |
| *支援的 Telethon SQLite 資料結構：7 及 8* / *Pyrogram … 2 和 3* | 此檔案是由非常舊或來源不明的函式庫版本所建立。請改用手機號碼／QR 碼登入。 |
| *僅支援經授權的生產環境使用者會話* | 該 Pyrogram 檔案屬於某個機器人或測試網路。 |
| *TData 存檔已超過 512 筆記錄或 32 MiB* | 僅包含 ZIP 檔案 `key_datas` 和 `D877F783D5D3EF8Cs`，而非整個資料夾。 |
| *無法解密 TData。請檢查桌面本機密碼* | 請在「**密碼」或「會話文字」**欄位中輸入 Telegram Desktop 的本地密碼。 |
| *每次僅可匯入一個 TData 帳戶* | Telegram Desktop 擁有多個帳戶；請參閱「[不支援的格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#unsupported-formats)」。 |
| *選定的檔案描述了不同的帳戶或 API 憑證* | 僅選取單一帳戶的檔案。 |
| *JSON 內容中未包含任何受支援的 API 憑證或授權資訊* | 請檢查 [Account JSON](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/#account-json) 中的欄位名稱。 |
| *僅限 API 元資料* | 該 JSON 檔案未包含會話資訊。請新增 `.session` 檔案，或使用手機/QR 碼。 |
| *授權金鑰的十六進位值必須包含全部 512 個十六進位字元* | 金鑰已被截斷或包含「`…`」。 |
| 帳號 ID 與匯入的帳號不符 | 該檔案的用戶 ID 與 Telegram 所顯示的不符；此檔案屬於另一個帳號。 |
| 該帳號已屬於另一個工作區 | 請開啟該工作區，而非重複新增該帳號兩次。 |
| 已連線，但「**來源」**中的聊天清單缺少一個私人群組 | 檢查會員資格。篩選器會檢查前 1,000 個對話；請在「**參數」**中提高此限制。 |
| 代理連線失敗 | 請檢查路由與 IP 模式。自動模式 MTProxy 會嘗試其他可用的入口。隱藏位址模式會進行等待；「直接」模式作為最後手段，可在設定的延遲時間過後直接連線。請參閱[路由模式說明](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/#ip-modes)。 |

另請參閱：代理伺服器與加密的[連線及安全性](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/)， 以及登入後資料擷取的[運作方式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/collection/)。
