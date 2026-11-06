# 已測試的內容

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/

Telegram 即時測試、自動化檢查、瀏覽器檢查，以及尚未經核實的內容。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [證據與驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/)

![證據與驗證](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**更新於 6 年 11 月 2026 日。**結果與每次執行所記錄的修訂版本、環境及 工作負載相關聯。[「當前功能](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md)」描述了 可用的工作流程；本頁面記錄了實際已驗證的內容。

[效能圖表](https://phishdestroy.github.io/TgWitness/docs/validation/) · [經簽署的英文審計報告](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [可下載的測量數據](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| 最新證據 | 結果 | 範圍 |
| --- | --- | --- |
| 版本審計 · 11 月 6 日 | 1,461 項核心測試通過；37 項平台測試跳過 | 來源 `92e539af40d8`；保留已公開的調查結果 |
| 最新匯出檔 · 11 月 6 日 | 127.713 和 141.781 筆/秒，完整週期 | 每台伺服器限兩個帳戶；文字與元資料透過 WARP 傳輸 |
| 保留的存檔 · 11 月 6 日 | 48 個檔案；已驗證 3,598,381 筆記錄 | 已將現有存檔與固定工作區金鑰進行比對 |
| Trusted Live · 11 月 5 日 | 受保護的 CPU 記錄與 WARP 檢查 | 官方桌面版登入功能與原生匯出功能仍未完善 |
| Phala / Intel TDX · 11 月 4 日 | 後續執行中，所有 16 項驗證器檢查均通過 | 歷史部署；CVM 上沒有 Telegram 帳戶 |

**本頁內容**

- [版本審計與最新匯出 · 6 年 11 月 2026 日](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu 與 WARP · 5 年 11 月 2026 日](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Phala Cloud 即時部署 · 4 年 11 月 2026 日](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [即時伺服器日誌清單 · 1 年 2026 月 2026 日](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [近期離線與故障注入檢查 · 1 2026 年 11 月 2026 日](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Telegram 即時測試，完整帳戶 · 29 年 10 月 2026 日](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [使用 libarchive 開啟的密碼保護匯出檔 · 29 年 10 月 2026 日](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Telegram 即時測試 · 2026年10月27日至29日](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [合成本地容量測量](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#synthetic-local-capacity-measurement)
- [對一百萬則訊息進行全文搜尋 · 5年11月2026日](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [剩餘資格說明](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#remaining-qualification)

## 版本審計與最新匯出 · 6 年 11 月 2026 日

本次審計採用原始碼版本 v0.9.1 `92e539af40d8368d198ff5e040f1d876f2c1310e`，發行版 `92e539af40d8-83e41104669e`。三台 伺服器均通過已安裝套件的煙霧測試。簽名報告保留了當時觀察到的狀態。

[![兩項新工作負載的擷取率與完整匯出率](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| 工作量 | 記錄 | 取得 | 完整週期 | 完整週期速率 |
| --- | --- | --- | --- | --- |
| 伺服器 A · 兩個帳戶 | 27,030 | 189.043 秒 | 211.647 秒 | 127.713 筆/秒 |
| 伺服器 B · 兩個帳戶 | 29,299 | 182.513 秒 | 206.650 秒 | 141.781 筆/秒 |

兩次匯出均未啟用「繼續傳輸」功能，排除附件與頭像，且最終 未產生任何重複或重複使用的記錄。完整週期包含準備、 擷取、篩選、封裝及存檔驗證。伺服器 A 亦執行了 受保護聊天室的讀取檢查。A 端發生四次 FloodWait 事件，B 端發生三次， 均獲得妥善處理。這些觀察結果並不能確立普遍的吞吐量保證。

| 檢查 | 結果 | 資格要求 |
| --- | --- | --- |
| 核心 pytest | 1,461 項通過 | 37 處平台跳過 |
| 瀏覽器 / 瀏覽器使用者體驗 / 證據 / 網站 | 102 / 66 / 15 / 9 項通過 | 這些程式與其他測試存在重疊；計數結果不可相加 |
| Capture 外掛程式 | 124 項通過 | 三項官方網頁檢查因必需的 Chromium 沙盒機制而受阻 |
| API 授權 | 269 條路徑；538 個請求通過 | 憑證遺失與存取權限遭撤銷 |
| 保留的存檔 | 48 筆中已驗證 48 筆 | 3,598,381 筆記錄；已釘選的工作區金鑰 |
| 即時車隊讀取檢查 | 40 個設定檔中有 24 個通過驗證 | 16條 WARP 路徑未通過資格認證；這些配置檔未建立連線 |

這份[經簽署的報告](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md)記錄了所有已公開的 發現結果，包括未公開的秘密聊天快照中存在的三項缺陷，這些缺陷 未出現在經審計的主建置版本中。先前 [針對公開歷史紀錄的](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md)評估採用了不同的 修訂版本和工作負載；其比率不得與本次比較結果合併。

請使用 [固定金鑰和驗證器](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files)來驗證原始報告。 其簽名可保護操作員的報告免遭篡改。這並非 獨立證明、Telegram 作者身份證明或 GDPR 認證。

## Trusted Live CPU Ubuntu 與 WARP · 5 年 2026 月 5 日

本次保留的整合執行環境採用了僅使用 CPU 的 Ubuntu 24.04.5.5 來賓系統（4 個 vCPU、8 GiB）， 在 RunPod CPU 主機內的 QEMU 環境中運行。資料收集器使用 `14e642a5`；驗證使用 `02072461`。最終的修正已合併至 [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) ，代號為 `755f78f6`，其代碼樹與測試中的 PR 頭部一致。此環境並非 TEE。

- 一個真實的 WARP Connector 報告狀態正常；經代理的 HTTPS 報告顯示 WARP 和 Gateway 已啟用。三個探測器觀察到相同的出站位址，這並不代表固定 IP 的保證。
- 斷開 WARP 連接導致代理請求失敗。直接連至閘道服務的 HTTPS 請求遭拒絕。在記錄器命名空間中，直接的 IPv4/IPv6、外部 DNS 以及 Docker 的內嵌 UDP 解析器均遭封鎖。
- 具有範圍限制的唯讀提供者代幣可讀取「健康狀態/連線」資訊，但無法 讀取連接器註冊代幣。簽署過的提供者觀察結果包含 明確標示為不可用的樣本。由於該見證程式運行於操作員的主機上，因此這 僅證明了記錄與保留功能，而非獨立第三方保管。
- 官方桌面版已進入未經認證的歡迎畫面。在擷取過程中，受保護的鍵盤 輸入遭拒。已解碼三個 H.264 顯示區段，並 檢查其時鐘疊加層。針對 18 個事件的預檢存檔，已 根據固定記錄器金鑰及保留的檢查點進行驗證。
- 最終的擷取測試在 Windows 和 Linux 持續整合環境中，使用真實的 Chromium/FFmpeg 通過了 114 個案例。五項錨點測試與依賴項警示檢查均已通過。

初始配置的 2 vCPU/4 GiB 環境在承受並發影像建置負載時發生超時， 並透過防護機制停止運作；此情況不被視為成功。手動測試帳號 登入、原生聊天記錄匯出、真實混合模式比較以及 Telegram 端登出功能仍 待處理。未導入任何提供的 Telethon 會話。附件、自動 OCR、 本地 drand BLS 驗證以及 Trusted Live TDX 證明均未通過資格審查。

## Phala Cloud 即時部署 · 2026 年 11 月 4 日

**歷史結果：**後續部署均通過所有16項驗證器檢查， 包括 Intel TDX 及快速隧道。重新啟動證據、簽名位址 發現及報告時間戳記均分別進行了檢查。每個測試 CVM 均 在執行完畢後被移除。

| 設定 | 記錄值 |
| --- | --- |
| 提供者 | Phala Cloud · `tdx.small` · US-WEST-1 |
| 部署 | `--provider phala --quick-tunnel`；初始工作區為空 |
| 初始收集器 | `df7d860c` · v0.8.1 |
| 包含所有修正的收集器 | `53a0f7e9` |
| 正式環境訪客 | `dstack-0.5.12`；SSH 存取已停用 |
| 外部服務 | ntfy.sh、GitHub 及 Intel PCS |
| 觀察到的成本 | 七種 CVM，總計約1.9美分；歷史測試定價 |

以下序列分別列出初始失敗、修正及已完成的檢查。 這些 CVM 未連接任何 Telegram 帳戶。

**部署版本 1–2 · 服務供應商差異與回歸測試**

前兩次部署發現與模擬的 Phala Cloud 有五處差異。 [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) 現已能重現每項差異，若未進行修正則會失敗：

| 在 Phala Cloud 上 | 修正前 | 修正 |
| --- | --- | --- |
| 必須指定 `compose_file.name` | HTTP 422 錯誤，未建立任何內容 | Docker Compose 配置中包含 CVM 名稱 |
| 除非指定為空，否則 Phala 會將其自身的啟動前腳本新增至被測的 app-compose 中（v0.0.20：Docker 登入、`docker compose pull`、root 密碼、來自 `user_config` 的 SSH 金鑰） | `tdx_compose` 失敗：程式碼超出已發佈的 Docker Compose 配置範圍 | app-compose 將 `pre_launch_script` 設定為 `""`；Phala 隨後會將其省略 |
| 若未指定 `image`，Phala 會預設選用 `dstack-dev-0.5.12`（開發版），且此版本已啟用 SSH 存取權限 | `server_state` 失敗。此映像僅有硬體驗證記錄通過；僅供應商記錄與 `tdx_os` 顯示此結果 | 部署過程會要求使用 Phala 當前版本（`dstack-0.5.12`）的生產環境建置版本 |
| 當 dstack 閘道器關閉時，CVM 詳細資訊中永遠不會出現 `instance_id` | 部署等待 30 分鐘後失敗 | 實例 ID 取自 CVM 狀態 |
| 重新啟動、停止及啟動均屬 CVM 操作，而非應用程式版本更新 | `provider_actions` 未列出重新啟動紀錄 | 這些操作也包含讀取操作 |

**部署3 · 認證、存取檢查與重新啟動證據**

- 該 CVM 在關閉 SSH 存取的情況下執行 `dstack-0.5.12`。收集器在建立後約 1.5 分鐘發布其簽名位址。部署後通過 `tdx_binding`、`tdx_quote`（Intel TCB UpToDate、硬體驗證記錄 v4、FMSPC `20a06f000000`、非除錯模式、不可遷移、支援從 Intel 擷取的 加密驗證資料）、`tdx_compose_hash`、`tdx_compose`（逐位元組）以及 `tdx_identity`（KMS 金鑰）。
- 位於 trycloudflare.com 網址的控制面板在未提供令牌或提供錯誤令牌時會返回 401 狀態碼， 而使用控制面板令牌時則會返回 200 狀態碼。
- `verify` 搭配 `--source` 設定為 GitHub 的提交存檔，且指紋已 另行通過：伺服器、`server_state`、防火牆（無閘道、無公開端點）、供應商日誌、 帳單明細、指紋、來源雜湊、開機，以及五項 `tdx_*` 檢查均通過。 Cloudflare 及 `tdx_os` 無法取得，因此結果為「不完整」。
- 透過 Phala 的 API 執行兩次重新啟動：每次 CVM 都在兩分鐘內恢復運作，並使用 相同的收集器金鑰、新的簽名位址，而舊的位址則回傳 530 狀態碼。`verify` 將 新的開機及兩次重新啟動皆報告為 REVIEW。 透過 `--evidence`，系統確認了日誌 簽名以及三次啟動，每次皆擁有來自同一 CVM 的獨立 Intel TDX 硬體驗證記錄。
- `destroy` 僅移除了該 CVM。隨後工作區變為空狀態，且控制台網址停止 回應。
- 控制台精靈的價格查詢顯示 `tdx.small`，每小時 0.058 美元。若輸入錯誤的金鑰，則會顯示 「未接受該 API 金鑰」的純文字訊息。

**後續修正 · 簽名位址偵測與作業系統測量**

- 若無地址金鑰，`verify` 會遵循關於地址主題的最新且格式正確的貼文， 該貼文印在已發佈的 Docker Compose 配置中。一則偽造的貼文將其傳送至一個不 存在的宿主，導致 `statement` 失敗：偽造者無法冒充收集器，但能阻擋 第三方驗證，透過偽造的未來時間戳記，最長可阻擋長達 12 小時。收集器現在 也會發佈以其自身金鑰簽署的地址，當 收集器發佈此類貼文時，`verify` 僅接受此類貼文，且貼文會依照 ntfy.sh 的接收時間排序。 [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) 會重播這些偽造的發布。CVM 僅會從包含此程式碼的提交中執行此程式，因此本次執行的收集器尚未簽署其地址， 而 `verify` 亦已指出此情況。
- `tdx_os` 原先依賴 `dstack-mr`，而該工具目前的版本提供的是 `measure-os`，並非文件中提到的 `measure --json`。驗證器現在會根據已發布的映像檔和虛擬機器設定（包含 ACPI 表格）自行計算 MRTD 和 RTMR0-2。

**部署4 · 所有16項檢查、報告封印及重新啟動驗證**

- 部署程序曾一次下載已發佈的 `dstack-0.5.12`，並將其與 CVM 回報的作業系統映像雜湊值進行比對，而 `tdx_os` 通過驗證：MRTD、RTMR0、RTMR1 及 RTMR2 均等於針對 QEMU 8.2.2、1 個 vCPU 及 2 GiB 所計算的數值相符。然而，針對聲稱具備 4 GiB、2 個 vCPU、 QEMU 9.2.1 或第二張網路卡的配置，相同計算方式得出的 RTMR0 數值則不同；若內核、韌體或命令列 發生變更，以及針對開發版映像，驗證均會失敗。
- `verify` 通過了全部 16 項檢查（包含快速隧道連接器），因此結果 為「通過」。 它寫入了 HTML 和 PDF 憑證，並以數位印章加蓋簽名與時間戳記，其中包含來自 比利時政府時間戳記單位 TSU 202301（已列入比利時可信 清單）的合格 eIDAS 時間戳記、FreeTSA 時間戳記以及驗證者的簽名；`check-report` 確認了所有這些 內容以及 PDF 文件的簽名。
- 重新啟動後，`verify --evidence` 確認了兩次啟動，每次均伴隨在 CVM 內部生成的硬體驗證，且每次 皆從已發佈的 `dstack-0.5.12` 啟動；重新啟動與新一次的啟動均為 REVIEW 狀態。
- `destroy` 使工作區保持空置狀態。

**部署版本5 · 由收集器簽署的發現機制與偽造貼文的拒絕機制**

此資料收集器自提交版本 `53a0f7e9` 開始運行，該版本已包含上述修正。

- 該收集器在其地址旁發布了以自身金鑰簽署的地址，緊鄰操作員的 HMAC 貼文。 隨後，該主題中新增了兩則偽造貼文，一則 HMAC 值為零，另一則由另一把 Ed25519 金鑰簽署，兩者均聲稱時間為 2096 年。 `verify` 採用由 收集器金鑰簽署的地址，並通過了全部 16 項驗證；該印章再次附有符合資格的比利時時間戳記、 FreeTSA 的時間戳記以及驗證者的簽名，而 `check-report` 則確認了這些資訊。
- 重新啟動後，收集器發佈了經簽名的全新位址：`verify` 立即偵測到該位址， 營運商的 **透過 HMAC 發佈，於 27 秒後偵測到當前位址**，兩者均忽略了 偽造的發佈。`verify --evidence` 確認有兩台裝置從 `dstack-0.5.12` 啟動。
- 部署過程列出了 Phala 向 CVM 收取的費用（含磁碟空間）：每小時 0.06078 美元。

### 面板精靈與剩餘範圍

面板精靈在 Phala Cloud 上執行了兩次，一次透過其工作 API，另一次則透過 搭載真實 Chromium 核心的瀏覽器：價格查核、以 **Advanced** 為提交標籤進行建立，全部六項 驗證檢查均通過，伺服器清單顯示計費價格（每月 44.37 美元）， **Find 當前位址**、下載已量測的 Docker Compose 配置，以及刪除操作。瀏覽器未出現任何頁面錯誤。 每次操作結束後，工作區均呈空狀態。

未涵蓋內容：Phala 上的 Cloudflare 網域、CVM 上的 Telegram 帳號，以及 `dstack-0.6.1` 映像檔。精靈在建立前的價格僅為 Phala 的運算價格，因為其 API 僅針對現有 CVM 列出 磁碟價格；伺服器清單則顯示建立後的計費價格。 本節中所有價格均於 4 年 2026 月 4 日觀察所得。

## 即時伺服器日誌清單 · 1 年 2026 月 2026 日

大約在 UTC 19:15，透過序列化的唯讀 SQLite `query_only` 查詢，統計了 正在運行的伺服器上十個工作區資料庫中的事件數量。在查詢期間， 資料收集仍持續進行，因此這並非橫跨所有工作區的原子快照。

| 在十個工作區資料庫中觀察到 | 計數 |
| --- | --- |
| 包含至少一個 `message.new` 事件的工作區 | 8 |
| 日誌記錄，包括運作事件 | 1,610,818 |
| `message.new` 事件 | 900,232 |
| `message.edited`事件 | 80,683 |
| `message.deleted`事件 | 400,536 |
| `message.recovered`事件 | 53,403 |
| `message.snapshot` 事件 | 2,183 |
| `media.saved`事件 | 50,418 |
| `media.failed`事件 | 5,575 |
| `coverage.gap`事件 | 11 |
| 資料庫位元組（不包含 WAL 檔案及媒體檔案） | 7,909,003,264 |

這些是 **事件計數**，而非唯一的訊息、使用者或媒體檔案。同一則 訊息可能出現在多個工作區中，且編輯或刪除操作可能會產生 另一個日誌事件。 `media.failed` 統計的是歷史失敗事件，而非 當前的媒體佇列。這些查詢並未 **不** 重新驗證簽名以及所有 紀錄的完整 1,610,818 記錄、測量傳送狀況或吞吐量，亦未確認 是否已擷取每個 Telegram 事件。此處未發布任何訊息內容、帳號或聊天室 ID、 工作區標籤、憑證或私人檔案。

在本次審查中，獨立配置的公開監測器涵蓋了三個來源： 其中一個擷取回應為「OK」，另外兩個則回報 `no_response`。該監測器 並非十個工作區的健康狀態摘要。`no_response` 表示觀察者無法 在該次檢查中取得回應；這並不代表訊息遺失。下方規模較小的 10月29日測試擁有其專屬的明確簽名與雜湊鏈驗證。

## 近期離線與故障注入檢查 · 1 年 11 月 2026 日

這些檢查使用虛構資料和本機檔案；它們為 當前來源提供回歸測試證據，而非針對其他實際運作中的 Telegram 傳送測量：

| 檢查 | 測試項目 |
| --- | --- |
| [原始檔案](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | 兩個建置版本的原始碼位元組內容完全相同，但檔案時間已變更，所產生的 ZIP 檔案及校驗和均相同。壓縮檔的位元組內容與檔案雜湊值完全吻合；私人測試檔案未被包含在內。模擬寫入失敗的情況下，先前壓縮檔及其校驗和均保持不變。 |
| [帳戶匯出與還原](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | 第二個 ZIP 成員發生模擬磁碟錯誤後，未產生任何已發布或不完整的 ZIP 檔案。恢復作業將每個簽名收據維持字節級別完全一致，並使用預期的簽名指紋產生可獨立驗證的壓縮檔，同時將合成覆蓋缺口保留為部分結果。規模斷言機制可防止隨著歷史記錄增長而重複掃描任務與收據。 |
| [最小化資訊披露以保障隱私](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | 在所有三種身分識別模式下，以及在文字省略的情況下，均已對合成 Unicode 名稱與別名、嵌套元資料、未知發送者及媒體欄位進行了檢查。遮蔽限制失敗並未在未經提示的情況下削弱遮蔽效果；原始的簽名帳戶匯出檔保持不變。 |
| [Linux 多媒體解碼器與 OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | 在提交 `5a9e0814` 時，[Linux Docker CI 檢查](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192)通過了以下項目：以 Ogg/Opus、MP3、M4A、含影片的 MP4、WAV 及 FLAC 為輸入的生成檔案；偽造時長與次級檔案參照的控制測試；以及 48 個變異解析器測試案例（34 個被拒絕，14 個在範圍內解碼成功）。真實的 Tesseract OCR 在原始位元組未經變更的情況下成功運行。解碼器與 OCR 均在網路隔離的容器中運行，且未使用 Whisper 模型。 |

這些檢查會在[「拉取請求」](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml)及 [「完整檢查」](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml)工作流程中執行。 它們旨在測試這些失敗邊界，而非每種可能的儲存失敗情況，亦非 評估洩露內容是否自動安全可發布。媒體檢查不會測量 語音辨識準確度或 Telegram 傳送狀況。分享前請審閱每個衍生內容。

## Telegram 即時測試，完整帳戶 · 2026年10月29日

在進行以下測試後，該帳號仍持續運作。10月29日 UTC 12:10，其監控範圍 已切換至整個帳號（頻道、群組、私人聊天室及機器人）；控制面板要求 確認，並由簽名日誌記錄此操作。截至 UTC 17:59，日誌內容如下：

| 記錄時間：10月27日 21:36 至 10月29日 17:59（UTC） | 計數 |
| --- | --- |
| 日誌記錄 | 9,968 |
| 新訊息 | 5,308 |
| 在切換至完整帳戶後，其中一部分 | 3,878 |
| 刪除記錄 | 784 |
| 其中部分訊息在 TgWitness 儲存該訊息後被刪除 | 596 |
| 編輯 | 41 |
| 經重新核對後新增的訊息 | 2,273 |
| 經重新檢查後已無法找到的訊息 | 18 |
| 透過歷史快照儲存的訊息 | 242 |
| 已儲存的附件 | 247 |
| 收集器啟動 | 19 |
| Telegram FloodWait 暫停 | 26 |

- 該小組的「**Verify」**核查已確認所有 9,968 筆記錄的簽名與雜湊鏈。
- 訊息來自 2 個群組或頻道，以及 3 個私人聊天室和機器人。其中有一次是在「**聊天室**」中 按下訊息按鈕；該請求及 Telegram 的回應均記錄於日誌中。
- 當收集器在重新啟動時重新掃描該帳戶時，新增了聊天室。由於 「儲存新聊天室的早期訊息」功能已關閉（`history = 0`），因此此處不予說明。

未涵蓋內容：反應、成員變動、個人檔案、發送訊息、透過 邀請加入、代理伺服器、通知、witness 機器人以及同時管理多個帳戶。公開檔案 僅包含計數資料。

## 透過 libarchive 開啟受密碼保護的匯出檔案 · 2026年10月29日

由匯出加密程式碼所建立的壓縮檔（WinZip AES-256 格式，7-Zip 和 WinRAR 可讀取），已透過 Windows 版 `tar`（bsdtar 3.6.2、libarchive）開啟。 輸入正確密碼後， 解壓縮後的檔案與原始檔案的 SHA-256 值相符；輸入錯誤密碼則會顯示「密碼短語不正確 」而遭拒絕。7-Zip 和 WinRAR 本身並未被執行。

## Telegram 即時測試 · 2026年10月27日至29日

一個真實的 Telegram 帳戶，透過內建的 API 配對池登入，記錄了某個 超級群組自 **10 月 27 日 21:36 UTC 至 10 月 29 日 05:15 UTC** 期間的訊息。在此期間， 資料收集器共啟動了 12 次。

| 已記錄 | 計數 |
| --- | --- |
| 日誌記錄，包含心跳訊號與服務記錄 | 2,385 |
| 新訊息 | 1,291 |
| 刪除記錄 | 472 |
| 其中部分訊息在 TgWitness 儲存文字後被刪除 | 347 |
| 編輯 | 12 |
| 暫停期間遺漏的訊息，已透過重新檢查補入 | 12 |
| 已儲存的附件 | 17 |
| 未下載附件（下載功能已關閉，或無檔案可下載） | 14 |
| Telegram FloodWait 在重新檢查時會暫停，每次暫停 3 秒 | 8 |

- 所有 2,385 筆記錄的簽名與雜湊鏈，皆可透過該日誌的 公鑰進行驗證。
- 重新啟動後，收集器將從儲存的更新狀態（`pts`）繼續運作，而 Telethon 會進行補齊；隨後的重新檢查則會新增仍缺失的訊息。
- 在每次 FloodWait 事件中，資料擷取器會等待指定時間後再繼續執行。
- 該帳號保持登入狀態，且同一會話於 10 月 29 日重新連線。

本次測試未涵蓋的項目：同時處理多個帳戶、管理員角色、代理伺服器、 持續數小時以上的服務中斷，以及完整的[即時驗收程序](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)。 公開檔案僅包含上述統計數據：不包含任何帳戶或聊天室識別碼、訊息或 憑證資訊。

## 合成本地能力測量

指令：`python tools/check_capacity.py --events 10000 --chats 100`

| 指標 | 觀察到 |
| --- | --- |
| 輸入 | 涵蓋 100 個精選合成來源的 10,000 則合成訊息事件 |
| 訊息內容 | 400 個字元；不含媒體或網路內容 |
| 資料擷取 | 53.273 秒；每秒 187.7 次事件 |
| 處理器延遲 | p50 4.162 毫秒；p95 7.784 毫秒；最大值 129.118 毫秒 |
| ZIP 匯出 | 啟用 tracemalloc 時耗時 19.868 秒 |
| Python 匯出區塊的峰值追蹤 | 0.51 MiB；不處理 RSS |
| ZIP 檔案大小 | 4,610,962 位元組 |
| 獨立驗證 | 所有 10,000 筆事件均已驗證 |

此測量針對本 Windows 主機上的本地序列記錄／匯出路徑。它 不測量 MTProto 傳輸、並行帳戶、Telegram 流量限制、媒體檔案、 長期運行的負載，亦不保證實際聊天數目。此測量是在 最終離線時間戳工具推出之前進行的，該工具並不會改變所測量的訊息路徑。

## 對一百萬則訊息進行全文搜尋 · 2026年11月5日

指令： `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

包含 200 個聊天室中 1,000,000 則合成訊息（俄語 詞形、烏克蘭語、英語、中文、日語、連結及識別碼）的確定性簽名日誌，於 71 秒內完成索引；該索引佔用 58 MiB 空間，此外還有 1.50 GiB 的日誌檔案。 最佳匹配 搜尋耗時 9 至 190 毫秒（中位數），相較之下，先前子字串 搜尋則需 2.4 至 3.2 秒。完整結果、硬體配置與限制：[全文搜尋](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#benchmark)。 `tools/test_fulltext.py` 亦會使用當前驗證器驗證在全文搜尋 （`tools/fixtures/evidence-before-fulltext.zip`）使用當前驗證器進行驗證，並使用該歸檔檔自身的 驗證器對當前 歸檔檔進行驗證。 `verify.py`.

## 其餘資格說明

所保留的即時日誌可記錄實際的訊息收集、編輯、刪除通知、附件、 重新檢查及速率限制處理。 它並未完整記錄訊息送達狀況，亦未建立受控的 角色可見性矩陣、反應主體、延長的 FloodWait、帳號封禁以及 網路／程序中斷恢復等資訊。QR 代幣的發行仍與已完成的 行動端 QR 碼確認程序有所區別。

Docker/Compose 及安裝檢查已記錄於 CI 中；實際的 Phala 部署 與外部時間戳記驗證已於上文說明。這些並未建立 持續的高負載、完整的實時平台／角色矩陣、獨立的安全 審查、長期歸檔驗證或鑑識認證。已實作儲存的 MTProto 狀態 與補齊功能；原子無損實時重播功能尚未建立。 較新的後補機制會以原子方式提交訊息與游標，並保留可用的 「近期操作」，但其合成覆蓋範圍有別於實時驗證。 有關受控驗證矩陣，請參閱[實時驗收部分](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)。

[公開審計目錄](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md)僅包含 已簽署的報告及彙總測量結果。詳細的操作紀錄、 原始擷取資料及帳戶資料仍屬私有。位於 `docs/assets/` 中的應用程式截圖使用虛構的示範資料。
