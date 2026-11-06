# Telegram · 功能與限制

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/

TgWitness 的現行蒐集模型、多帳號工作流程、匯出功能及操作範圍。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [專案參考資料](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![專案參考](https://phishdestroy.github.io/TgWitness/assets/chapter-project.svg)

TgWitness 可保存連線帳戶可存取的 Telegram 對話內容， 記錄觀察到的變更，並準備可驗證的匯出檔案。本參考文件說明 資料蒐集模型、現行工作流程及其範圍。

**本頁內容**

- [獨立應用程式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#standalone-application)
- [共享調查](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#shared-investigations)
- [歸檔工具](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#archive-tools)
- [可選附加內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#optional-extras)
- [協定與私有來源](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#protocol-and-private-sources)
- [多個帳戶](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#multiple-accounts)
- [擷取與來源標示](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#capture-and-attribution)
- [容量與 Telegram 限制](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#capacity-and-telegram-limits)
- [可靠性與恢復](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#reliability-and-recovery)
- [證據模型](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#evidence-model)
- [匯出、部署與移交](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#export-deployment-and-handoff)
- [穩定版發布標準](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/features/#stable-release-criteria)

## 獨立應用程式

TgWitness 擁有專屬的安裝程序、資料目錄及發行週期。內建的 網頁介面負責設定與檢視；匯出的記錄可獨立使用。

操作者可連結其帳戶、選擇彼此可見的來源，並取得 一份儲存的觀察日誌。控制面板會顯示內容、已儲存的變更、觀察 來源及已知缺漏。其他調查人員可驗證匯出的資料。

該面板區分帳戶授權、來源存取權限、收集器 活動及記錄範圍。在評估 訊息較少或出現連線問題的區間時，請一併檢視這些狀態。

## 共享調查

管理員可發行範圍限於工作區及 個別聊天室的[存取憑證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/)，並可設定每項操作的權限、IP 限制、有效期限、登入次數限制 及會話控制。唯讀審查員無需取得 Telegram 授權或主面板金鑰，即可檢視案件。 僅限聊天室的存取權限 與全帳戶設定及完整日誌匯出功能相互獨立。

自動 MTProxy 會從四個公開來源或 營運商目錄中維護可運作的 Telegram 路由。[IP 模式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/#ip-modes)決定 當發生故障時，系統是否必須等待另一個代理伺服器，或是可使用明確允許的直接路由。 外部 HTTP 請求擁有獨立的路由及關閉開關。

## 歸檔工具

0.7.1 包含[歷史紀錄擷取](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/history/)、[檔案庫搜尋與分析](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/analysis/)、[唯讀 MCP](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/mcp/)、[本地 OCR／轉錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/media-analysis/)以及[外發 webhook](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/webhooks/)功能。分析報告與辨識出的文字將與 擷取的事件分開儲存。

[「案件看板」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-board/)可在工作區內新增與來源連結的書籤、引文、筆記及 彙整集。[報告建構器](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-reports/)可選取 素材、章節，並從八種設計中選擇一種，以支援 HTML/PDF 匯出。

## 可選附加功能

日常設定流程為：帳戶 → 來源 → 監測。**額外功能**為獨立的目標選項， 包含 Telegram 證據記錄機器人及 GitHub 擷取預覽。各選項會在顯示 設定前，先說明其可用性與需求。點選卡片會開啟操作說明；此動作不會進行註冊或啟動服務。

機器人設定包含三個步驟：建立唯讀存取權限、選擇發佈設定，以及 在 Witness 主機上啟動。網路與發佈選項、現有連線及 驗證指令將依需求顯示。 下載的配置檔與 正在運行的 Witness 實體不同。切換附加功能時會保留草稿；帳戶變更及鎖定 操作則會清除臨時憑證與表單。內建指南包含啟動說明。 [GitHub Actions 會](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)從您的 分支啟動一個固定收集器，擷取一個聊天記錄，並產生包含工作流程來源資訊的加密交接檔。

## 協議與私有來源

**MTProto 是 Telegram 的通訊協定；Telethon 則是 TgWitness 用於 與 MTProto 通訊的 Python 函式庫。**這兩者並非替代性的連線方式。「收集」功能使用 MTProto； 而可選的「見證者」則透過 Bot API 發佈經簽名的檢查紀錄。

每個工作區皆擁有專屬的授權客戶端及帳戶更新串流。TgWitness 會從已設定的來源中篩選觀察結果，並針對歷史紀錄快照與媒體下載等功能， 分別發出明確的請求。

私人消息來源無需公開使用者名稱。Telegram 的對等節點類型與數值 ID 才是 識別標識；標題與使用者名稱皆可能變更。存取權限取決於現有的 會員資格與權限設定。TgWitness 不會自動加入消息來源，也不會繞過 加入審核。來自其他帳戶的存取雜湊值並非通用存取憑證。

資料蒐集模型必須涵蓋加入群組前的隱藏歷史紀錄、參與者／管理員 角色、會話撤銷、權限移除或變更、群組轉為超級群組 的遷移、主題／論壇、關聯討論、頻道身分以及無法存取的 附件。並非所有組合皆已通過實際運作驗證。

來源可見性會在收集器啟動時進行檢查。若在限定範圍內的 對話結果中缺少某個來源，表示**該來源的存取狀態未經確認**，而非已證實遭刪除。即使有一個 來源不可用，也不會影響對其他可存取來源的監測。切勿將邀請 連結或真實會話內容放入公開的測試資料中。

## 多個帳戶

該面板支援任意數量**的工作區**，每個工作區皆具備：

- 授權機制、加密儲存庫及連線路徑。
- SQLite 日誌及 Ed25519 簽名憑證。
- 精選來源、媒體佇列及擷取設定。
- 監測狀態、錯誤、檢查點及匯出功能。

切換顯示的工作區並不會停止其他資料擷取器的運作。跨工作區的重複帳戶 授權將被拒絕。已綁定至某個 Telegram 帳戶的日誌無法重新指派給其他帳戶；但允許重新連線至同一帳戶。 此舉可確保帳戶身分及相關訊息 ID 範圍的完整性。

本應用程式未設定固定的工作區數量。每個工作區皆在 共享的 Python 程序與事件迴圈中，執行其專屬的收集器 任務，包括連線監控、媒體下載、重新檢查及新聊天室匯入。處理量取決於工作負載。為 實現程序隔離，請使用獨立的安裝、連接埠及資料目錄。

為每個帳戶指派其可存取的來源。不同帳戶可能觀察同一個 群組，但其觀察記錄仍保持獨立，並保留原始來源。同一台由操作員控制的機器上的兩個帳戶 並不構成兩個獨立的證人。**匯出群組時，** 會將分別簽署的工作區 ZIP 檔與一份簽署的檔案清單打包，該清單包含其 工作區 ID、雜湊值及簽署金鑰指紋。 每個日誌皆保留其自身的 邊界。可在案件筆記或分析工具中建立跨工作區的綜合時間軸， 並保留這些來源參考資訊。

## 擷取與來源標示

「來源」功能提供針對各帳戶的新訊息、編輯、刪除、反應 及成員資格的切換選項。預設設定可選擇保留所有類別，或僅保留訊息／編輯／刪除記錄。 此政策適用於工作區中選定的群組，重啟後仍會保留，並會 以變更前／後的狀態進行簽署。預設設定為保留所有類別。 關閉某個類別 不會移除舊記錄；重新開啟該類別也不會重建遺漏的事件。 操作記錄、其他群組服務事件以及明確的歷史快照均屬 獨立項目。擷取的 Telegram 物件可能會保留內嵌的元資料，無論 「獨立更新」開關的設定為何。目前尚無針對各群組的類別覆寫功能。

| 資料 | 立即擷取 | 分隔線 |
| --- | --- | --- |
| 訊息 | 文字內容、同儕/訊息 ID、發送者元資料、回覆內容及原始更新封套 | 以「由收集者簽署、帳戶可見的觀察記錄」形式保存 |
| 編輯 | 新觀察到的版本以及任何先前儲存的版本 | 系統停機期間的中間編輯內容可能會遺失；發送者未必就是編輯者 |
| 刪除 | 通知及先前擷取的內容（如有） | 通常不包含刪除者或確切的操作時間 |
| 帳戶層級刪除通知 | 原始通知；已解決的紀錄包含儲存的聊天內容及關聯分析方法 | 範圍內必須精確包含一個先前已儲存的「私人聊天」或「一般群組」配對；其他 ID 將保留為「`deletion.unscoped`」。頻道和超級群組的 ID 不包含在此關聯範圍內 |
| 反應 | 已交付的計數器及可見的近期身分資訊 | 完整的可用反應器清單需另行查詢；頻道可能會隱藏身分 |
| 會員 | 服務訊息及已送達的參與者更新 | 可見性取決於角色與聊天類型；事件缺失並不代表該事件不存在 |
| 管理員操作 | 相關已交付更新及管理員日誌快照，皆包含於頻道／超級群組聊天記錄的匯出檔案中 | 匯出功能會在匯出管理員帳戶可存取時讀取日誌；持續輪詢管理員日誌的功能不屬於此流程範圍 |
| 附件 | 原始版本描述、下載位元組數／SHA-256 及嘗試結果 | 已消失的檔案可能無法恢復；最新版本不會被替換 |
| 歷史沿革 | 當前可見訊息的明確快照 | 不會還原所有編輯或刪除的內容 |
| 收集程序 | 啟動／停止、心跳訊號、錯誤、設定、範圍及簽名執行收據 | 本地清單；GitHub 與 TDX 新增[獨立環境檢查](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope) |

介面會標示來源事件中提供的帳號，並保留觀察到的 名稱與使用者名稱。當事件未標示行為者時，報告會將該欄位留空。

## 儲存容量與 Telegram 限制

目前尚無能保證監控品質的通用聊天室數量標準。 監控容量取決於每秒的峰值事件數量、附件數量與大小、額外的 RPC 請求、活躍帳戶數量、磁碟延遲／可用空間、網路狀況、Telegram 的限制、 可接受的延遲以及佇列深度。

Telegram 將「被動傳送」與「主動短輪詢」區分開來。其更新 文件中說明，針對公開 頻道／超級群組會產生額外的 `updates.getChannelDifference` 呼叫，並建議**同時進行短輪詢的 來源**最多為十個。這並非指僅能選取十個群組，亦非完整性保證。

| 模式 | 目的 | 狀態 |
| --- | --- | --- |
| 標準觀察 | 記錄來自選定來源的已發佈更新 | 已實作 |
| 優先級複核 | 已標記的來源採用其自身可配置的間隔，並在每次限定範圍的重新檢查循環中具有優先權 | 已實作歷史紀錄與訊息查詢功能 |

優先級星號用於控制這些重新檢查。額外的 ``updates.getChannelDifference` ` 短間隔輪詢功能不會作為獨立的使用者模式對外公開。

任意的高頻率輪詢、忽略 FloodWait 設定，或假設額外帳戶具備線性處理能力， 均非有效的規模估算模型。預設限制為 前 1,000 個列出的對話，每個歷史快照最多 500 則訊息， 每種類型的收集檔案為 1–2,000 MiB，以及 4 GiB 未壓縮的簽名 ZIP 內容；各項 限制皆可於**「參數」**中針對各工作區進行調整。匯出資料無固定事件數上限。 瀏覽器備用模式預設上限為 128 MiB；串流 CLI 具有可配置的 傳輸限制，預設為 5 GiB。

## 可靠性與資料復原

已實作的功能包括 SQLite WAL／同步交易；原子性訊息 與媒體處理任務寫入；持久化任務與重試延遲；原始版本描述符； 有限重試；媒體 FloodWait 的持久化；在文字事件的 網路等待之外進行媒體下載；在後續寫入持續進行時進行穩定前綴匯出；原子設定與 稽核記錄；在替換登入失敗後保留有效授權； 受損附加工作區的隔離；顯式重新連線嘗試；明確的 授權喪失通報；以及使用單調時鐘進行的實時時鐘變更偵測。

帳戶與頻道的 pts/qts/seq 值會在重新啟動後保留並恢復，且受監控的聊天室 會定期重新檢查；詳見[證據格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#durable-collection-and-process-receipts-02)。定期儲存位置 並非對日誌接受的原子性、無損確認。

每次流程啟動時，都會記錄前一個頭部位置與離線邊界。當前的歷史紀錄 不被視為缺口修復。Telegram 的差異保留容量是有限的； `differenceTooLong` 無法重建所有已消失的內容。即使後續的歷史快照成功，不可恢復的缺口仍須 明確標示。

## 證據模型

每項事件皆記錄事件序列、當地 UTC 觀察時間、來源時間（若提供）、 事件類型、來源、行為者（若提供）、原始載荷、前次雜湊值及簽名。 訊息觀察記錄亦會保留收集者帳戶／執行上下文。

該簽署的處理收據包含隨機生成的執行 ID；TgWitness/Python/OS/依賴項 版本；原始檔的 SHA-256 值與彙總指紋；初始帳戶、 範圍及設定；UTC/單調讀數；以及前一則日誌的開頭。 設定變更、啟動／停止及錯誤訊息均會記錄於同一日誌中。檢查點會 於啟動時、監測期間每五分鐘（可調整）以及正常停止時保留。 保留的本地檢查點可偵測是否回滾至較早的日誌前綴。

| 運作機制 | 其功能說明 |
| --- | --- |
| 檔案 SHA-256 | 位元組與已知摘要相符 |
| 事件雜湊鏈 | 記錄相對於已知邊界的排序／關聯性 |
| Ed25519 | 特定金鑰下的簽名 |
| 獨立保留的檢查點 | 後續內容與保留的範圍一致 |
| 程式檔案大小測量 | 關於已測量檔案的收集器自我報告 |
| 有效的獨立 TSA 回應 | 在明確的信任假設下，特定時戳（TSA）時間點下特定位元組的存在性 |

已實作 RFC 3161 請求準備及 OpenSSL 回應驗證功能。 「證據模式」亦會將檢查點雜湊值提交至已設定的時間戳記服務。 請保留並驗證主管機關的回應，以建立獨立的時間錨點。 請參閱 [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/timestamp/)。

獨立保留檢查點、控制簽署金鑰的存取權限、保存傳輸 紀錄，並使用可信賴的軟體驗證匯出檔案。[驗證範圍](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope) 說明了這些檢查如何相互補充，以及適用哪些信任假設。

## 匯出、部署與移交

經簽名的 ZIP 檔案包含原始的 JSONL、CSV、HTML 檔案、保留的附件、雜湊值、一份 經簽名的清單以及一個便捷驗證工具。其涵蓋一個工作區及一個固定的完整 日誌前綴。面板搜尋篩選器不會在未經提示的情況下移除記錄。 密鑰、 憑證及 Telegram 會話均不包含在內；原始記錄仍可能包含 個人資訊及 Telegram 元資料。

請將 ZIP 摘要、可信指紋、檢查點、處理收據及交接 記錄分別保存。應使用來自可信安裝來源的驗證器，而非僅因可執行 程式碼出現在被檢查的 ZIP 檔案中，就直接信任該程式碼。

瀏覽器介面可本地部署，無需 Node.js、CDN 或外部字型。一個 操作員憑證即可控制整個安裝過程。遠端存取需透過 HTTPS 或 SSH 隧道進行。 提供原生 Python 程式碼及容器定義，部署範例位於 [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 目錄下；已執行的平台檢查項目則另行列出。

預設工作區使用資料根目錄；額外的工作區則使用 `profiles/<id>/`。 備份需先停止程序，並備妥完整的資料／金鑰組。證據 ZIP 檔 並非應用程式備份。機密資料可使用外部主金鑰來建立新的資料 目錄；日誌／媒體加密則由操作者的磁碟／磁碟區提供。 請參閱 [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/connection/) 及 [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/operations/)。

## 穩定版本發布標準

在穩定版發布前，請補充說明：

1. 真實的私人群組、超級群組、論壇及頻道，包含成員／管理員角色，以及 隱藏／可見的歷史紀錄，涵蓋登入／雙因素驗證、權限撤銷及存取權限喪失等資訊。
2. 針對已知行為，對編輯、刪除、反應、成員資格及媒體內容進行監控。
3. 流程／主機當機、磁碟故障／磁碟空間已滿、檔案參照過期、FloodWait、 網路中斷、檔案損毀及資料庫回滾。
4. 支援持續的多帳號使用，並可控制延遲、佇列、記憶體及磁碟資源，包含 同時處理靜態與動態資料來源。
5. MTProto 狀態推進與日誌接受之間的間斷。
6. 在目標作業系統／容器組合上進行乾淨安裝，並驗證備份與還原功能。
7. 針對安全性、簽名以及來源歸屬／證據主張的獨立審查。

「[存取與權限](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/access/)」章節中說明了分域式面板存取權限。0.6 版支援 [《ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/)》中所述的「有限單一帳戶 TData」及「帳戶檔案匯入」功能。 發佈前請詳閱 Telegram API 條款。相關研究參考資料及平台 調查結果請參閱[《RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md)》。
