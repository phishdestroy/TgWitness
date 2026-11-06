# 報告配置與驗證

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/case-reports/

報告篩選器、八種設計範本、內容預設值、已儲存的變更歷史紀錄，以及簽署後匯出檔案中所包含的評估結果。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

將選定的觀察結果轉化為敘述案件的易讀報告：包含案件問題、 範圍、已儲存的變更、圖表、調查結果及來源參考。每份報告皆提供 收件者一種方式，用以核對所交付的資料，並檢視其蒐集 範圍。

「**信任基礎與限制**」章節會出現在日誌、移交、聊天、 帳戶及分享報告中。日誌與移交的 PDF 檔案採用與 其簽署過的 ``report.json`` 相同的評估結果。ZIP 清單在簽署過的 清單中包含 ``case_assessment``。此評估結果會隨同匯出的資料一併傳遞。原始 觀察結果則保留其現有的簽名。

## 文件格式與閱讀順序

### 報告工作室

開啟**「匯出」→「設定」並預覽**。依序操作**「資料」→「設計與內容」→「預覽**」：

1. 可使用整個工作區，或選擇聊天室、發送者，並包含 UTC 觀察 日期及事件類型。載入目錄以搜尋聊天室和發送者，或直接輸入 其 Telegram ID。發送者篩選器會比對已記錄的發送者 ID；若刪除 通知未標示發送者，則不會與發送者篩選器匹配。
2. 選擇一個頁面設計，接著選取圖表、參與者標籤、對話紀錄以及 您撰寫的調查結果。變更設計時，這些選項將予以保留。
3. 建立預覽畫面。該畫面會顯示實際計數、活動狀況、參與者、範例 紀錄、已儲存的變更以及缺失的訊息編號範圍。若變更選項 ，預覽畫面將標示為過時。請在下載 HTML、簽名 PDF、 簽名 JSON 或證據 ZIP 檔案前先儲存。

資料預覽所統計的是完整的穩定日誌前綴，而非初始樣本。 僅顯示的樣本列與長清單會被截斷；其省略的計數會 一併顯示。後續匯出將擷取新的穩定快照，因此持續的蒐集作業可能會 增加相關數字。範圍、計數及來源身分均包含於 經簽署的報告中。開啟或預覽表單並不會將其儲存。

**Jurisdiction guidance.** Under Document details, open **Jurisdiction guidance · optional** to choose a jurisdiction and civil/commercial or criminal procedure. The appendix carries the legal basis, source links, preparation notes and research status. Local-language summaries and explanations of collection safeguards are optional. No jurisdiction is selected by default. These choices belong to the workspace, and are excluded from saved layout configurations and implicit sharing-copy defaults. See [defaults, supported reports and research limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/JURISDICTION_GUIDANCE.md).

**請選擇收件者的副本。** 圖表和對話紀錄均採用所選的紀錄。 完整性、保管與涵蓋範圍描述了完整的原始日誌。證據 ZIP 檔案 包含其原始紀錄及附件。當收件者僅需接收經選取且獲准的資料時，請採用[精簡版移交流程](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#handover-extract) 。

### 讀取編輯、刪除及缺失的 ID

編輯操作會顯示儲存前的**「**原始**」**與**「修改後」**文字，並標示出變更的 詞彙。刪除操作則會顯示通知出現前最後儲存的版本。若未擷取較早的 內容，報告中會明確註明。當您僅篩選編輯或刪除操作時， 先前版本仍會作為明確標示的上下文，在 篩選器之外保留供查閱。 無關的訊息不會被加入這些歷史紀錄中。

**未觀察到的訊息 ID** 是指在選定的聊天室中已知編號與 根據日期衍生的 ID 範圍之間存在的空缺。在將某個 編號宣告為未觀察到之前，必須先檢查所有已知的來源記錄：篩除另一位發送者、事件類型或日期， 均不會造成虛假的空缺。 相鄰的已儲存訊息會被標記為「上下文」。缺少 一個數字並不能證明該訊息曾經存在或已被刪除；刪除通知 與重新檢查失敗仍屬不同的事件類型。

### 選擇設計

提供八種頁面設計，適用於日誌、單一聊天記錄的 HTML 及簽名 PDF 報告。這些設計使用相同的記錄資料與計算結果，僅在封面、 排版、章節標題、表格及行距方面有所不同。

| 設計 | 行文風格 |
| --- | --- |
| 經典版 | 一份採用深色封面且各章節編有編號的傳統檔案夾。 |
| 編輯說明 | 採用帶框的襯線體標題頁、寬邊距及窄版章節欄。 |
| 簡報 | 採用簡潔的封面設計，書脊為海軍藍色，標題簡短，表格排列緊湊。 |
| 分析 | 採用問卷式封面、模組化圖表版面及等寬字體的圖表。 |
| 技術 | 包含橫線登記表、編號參考欄及精確的比對表格。 |
| 概述 | 全景式封面、寬敞的版面間距以及醒目的摘要圖表。 |
| 閱讀系列 | 內容架構包含側邊欄，並將「調查結果」、「範圍」、「變更」及「觀察日誌」等章節分組呈現。 |
| 帳本與保證金 | 章節應採用編號形式並留有寬邊距，圖表須精確呈現，且訊息紀錄應獨立成篇。 |

設計會依工作區分別儲存，並記錄於已簽署的匯出清單中。 HTML 支援離線使用、淺色與深色主題，並能適應窄螢幕 及由右至左的語言。原生 PDF 採用內建字型；編輯版面設計 包含 Noto Serif 字型，並受其內建的 SIL 開放字型授權條款規範。閱讀系列以及 「帳本與邊距」功能亦適用於帳戶概覽、帳戶聊天室及分享副本。

若需處理中文、日文及韓文的 PDF 檔案，伺服器上需安裝合適的字型， 例如 Noto Sans CJK，該字型需安裝於系統全域，或放置於 `TGWITNESS_FONT_DIR` 目錄中。 若無法取得該字型，ZIP 檔案將保留 HTML 及 JSON 格式的報告。

這兩種設計包含無需 JavaScript 即可閱讀的日誌。針對大型 匯出檔案，此檢視畫面在 8 MiB 的輸入配額內最多可顯示 500 筆完整紀錄； 報告會標示此限制，並提供連結至完整檢視器及原始紀錄。 帳戶目錄與關係索引描述的是同一份閱讀樣本， 而非所有參與者。完整日誌圖表則維持其獨立標明的範圍。

### 選擇內容

| 目錄預設 | 預設包含 |
| --- | --- |
| 案件檔案 | 活動、觀察時間、參與者、聊天內容及對話紀錄。 |
| 簡報 | 活動概覽，不含參與者排名或對話紀錄。 |
| 活動審查 | 活動、觀察時間、參與者、聊天內容及其組成，並附上來源參考及確切數字。 |
| 自訂報告 | 請自行組合圖表、對話紀錄與預覽內容。 |

變更預設值時，您的設計、案件詳情及書面分析將予以保留。完整性 檢查、涵蓋範圍、限制事項及驗證說明將保留於每個設計中。 當圖表或文字記錄被隱藏時，ZIP 檔案中的原始記錄將保持不變。

可選的「**檢查筆記**」包含報告作者撰寫的提問、方法、發現結果及 結論。在發現結果中須引用原始檔案及記錄編號。 簽名機制將這些作者陳述與報告一併保存；原始觀察結果及作者的詮釋仍可被識別。 簡化版交接文件會省略這些私人筆記及完整的病歷圖表。圖表與 檢查選項同樣適用於病歷報告。

可篩選特定時間段的活動、UTC 工作日／小時熱力圖、參與者排名、聊天 排名及記錄組成。選擇 5 至 30 個排名組別，以及中立的參與者 別名或帳號 ID。未知發送者與其餘參與者將顯示於 獨立的行中。別名僅影響圖表顯示；原始記錄仍包含其真實身分。

設計預覽會根據未儲存的草稿進行更新，並採用正式版封面、檢視及 圖表元件，僅限於前 50,000 筆來源記錄中的匹配項目。下方的資料預覽 則會計算完整的選取範圍。此預覽明確 標示為「未簽署」，且不會保留編輯內容。「封面」與「圖表」按鈕可切換其區段。 這並非完整的 PDF 預覽。**「儲存報告設定」**會將選項套用至 未來的匯出；現有的已簽署檔案則不可變更。PDF 會使用所選的封面、 排版、章節佈局，以及與 HTML 和已簽署 JSON 相同的彙總項目。

信任評估、涵蓋範圍限制及驗證說明仍須保留。 隱藏圖表或可讀文字記錄並不會從 ZIP 檔案中移除權威來源資料行； 已停用的圖表系列將從分析用 JSON 檔案中省略；請使用 「最小化匯出」功能以限制來源記錄的揭露範圍。

資料篩選濾鏡適用於日誌報告；帳號與分享內容的匯出檔將保留 其自身的蒐集與揭露範圍。

共享的設計／圖表偏好設定將被鎖定於新的聊天室／帳戶匯出檔及帳戶 共享預覽中。帳戶／共享的語言與隱私設定仍保持獨立； 私人案件及審查筆記不會被複製至這些匯出檔中。帳戶與 共享報告仍以 HTML 格式儲存，並透過其簽名存檔清單受到保護。 日誌、 精簡版日誌移交及單一聊天套件亦提供經簽署的 PDF 檔案。

### 圖表所呈現的內容

日誌活動與熱力圖會根據收集器的觀察時間（UTC）統計新訊息、歷史訊息、已復原訊息、已編輯訊息、已刪除訊息以及 重新檢查時缺失的**觀察記錄**。心跳訊號 與附件收據不包含在內。 參與者排名僅統計新、歷史 及恢復的訊息觀察記錄：發送者不會被標記為編輯者或 刪除者。重複的觀察記錄可能描述同一則 Telegram 訊息。

日誌分析功能會保留各類別的計數、首/末筆記錄參考，以及來源檔案 `events.jsonl` 的 SHA-256 值。圖表中的數值在 HTML 和 PDF 格式中均為精確數值。每日區間 在記錄超過 366 天後會切換為按月區間；圖表會將這些區間合併為最多 36 個等寬區間。 若存在超過 100,000 個不同識別碼或 1,200 個月的標記， 相關圖表將無法顯示，但確切的總計數值仍可查閱。

快照與帳戶共享圖表僅計入所包含的非服務訊息列， 並採用其記錄的訊息時間。共享彙總值是在遮蔽 與篩選後計算得出。這些圖表最多使用 90 個等寬的 UTC 日期區間，並保留 最多 10,000 個分組值；超出數值會明確標示並進行核對。 最後一個區間可能較短。未知或原始日期不會納入時間圖表中。

若區間為空，表示未包含任何觀察記錄；如有缺口，請參閱覆蓋範圍。這些 圖表描述已儲存的活動。未知發送者仍歸類為獨立類別，且 每項檢查均會單獨報告。

若包含 `analytics.json` 檔案，該檔案將受存檔的簽名檔案雜湊值保護。 日誌 `report.json` 嵌入相同的選取彙總值。簽名驗證 可偵測字節變更。若要核對數值，請使用 `report_analytics.Analytics` 和 `selected` 重新計算日誌彙總值，或 使用 `snapshot_analytics.collect` 和 `project` 重新計算快照彙總值。

### Anomaly indicators

**Preview.** Evidence reports add an **Anomaly indicators** section computed by registered processors (`tgwitness/metrics/`, one file per metric). The report names every processor that ran with its version, and prints its method under its table, so the computation can be repeated from `events.jsonl` with `tgwitness.metrics.run`.

| Processor | 功能展示 |
| --- | --- |
| `first_time_posters_over_time` v1 | First-time posters and messages per UTC day. A flag requires at least five first-time posters and three times their median, with message volume at most 1.5 times its median. The baseline uses at least seven observed days within the previous 14 calendar days, after seven days of warm-up. |
| `service_vs_message_ratio` v1 | Distinct saved message numbers per chat and the share used by service messages. It describes a numbering; it does not explain a particular missing number. |
| `join_leave_per_month` v1 | Joins, departures and removals or bans per month, one per person, chat, change and day. |
| `pinned_per_month` v1 | Pin service messages, unpin notices, and pinned messages added or removed between chat-state snapshots, per month. |

**Parameters → Report metrics** selects processors and the number of displayed rows, including in filtered reports. Daily and monthly tables show recent rows, service-share tables rank chats by saved message count. Totals cover every row.

請從原始碼檢出點開始，根據同一份虛構期刊，建置上述列出的全部八種設計：

```
python tools/build_report_styles.py --output test-results/report-styles
```

開啟生成的 `index.html` 檔案，以比對完整的 HTML 報告、已簽名的 PDF 檔案及 ZIP 檔案。每個設計皆採用相同的原始日誌。每次執行時請使用新的輸出目錄， 以便保留先前已簽名的範例。

![虛構的 HTML 檔案](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

HTML 頁面以案件封面及關鍵數據開頭。編號的證據地圖連結 至各項調查結果、其支持事實、限制條件及獨立審查報告。可搜尋的 紀錄與穩定的紀錄參考資訊，在離線檢視器中仍可使用。 此設計可適應窄螢幕，並相容於各種主題及無需 JavaScript 的瀏覽器。

已簽署的 PDF 文件包含專用的 A4 封面、報告參考編號與 QR 碼、執行 摘要、證據地圖、編號調查結果及文件書籤。其頁 首與頁尾標示了報告資訊。QR 碼用於識別資料來源；它並非 獨立的驗證結果。瀏覽器列印輸出與此 經加密簽署的 PDF 文件是分開的。

觀察時間軸將記錄的觀察期間與中斷 置於同一條 UTC 軸上。空白處不代表推斷出的覆蓋範圍；詳細表格 保留了確切的時間間隔。ZIP 檔案包含可讀取的報告、已簽名的 JSON、 來源記錄及驗證說明。

請生成一份全新的虛構英文／俄文／德文檔案，並假設已安裝開發 環境：

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

每個語言目錄均包含 `report.html`、`report.pdf`、`report.json` 及 `dossier.zip`。現有的範例目錄絕不會被覆寫。建立這些檔案時，不會使用任何 Telegram 帳戶、外部時間戳記服務或網路連線。

![虛構簽名 PDF 文件的前三頁](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## 閱讀具體案例

以包含 1,200 筆記錄的日誌為例，其中第 1,000 筆記錄具有經驗證的時間戳記， 報告指出有 200 筆較晚的記錄超出該時間戳記的範圍。 這僅是 檢查點存在的上界，並非每則訊息發送 時間的證明。若另有三個時間戳記檔案驗證失敗或無法驗證， 則會另行計數，且無法作為肯定結論的依據。

一個可用的時間戳記必須通過所有以下檢查：其印記與 檢查點相符；其簽名鏈在加蓋時間戳時可追溯至可信的 TSA 根；且 檢查點的簽名、金鑰、計數與頭部與日誌前綴完全吻合。 僅解析時間戳記或持有 OTS 收據並不足夠。讀取者 必須獨立選擇可信的 TSA 根憑證，並重複驗證。OTS 需要 其專屬的比特幣確認檢查。

| 報告狀態 | 含義 |
| --- | --- |
| 已於匯出時進行檢查 | 匯出工具已執行所述檢查；仍需進行獨立重複驗證。 |
| 已記錄；需進行審閱 | 所記錄的是基礎觀察結果或操作員陳述；這並非獨立確認。 |
| 本譯文未包含以下內容 | 該內容並未提供支持此主張的佐證。文中亦未提及其他地方不存在此類佐證。 |
| 未經獨立核對 | 本報告不提供獨立的驗證結果。 |
| 不完整或無法取得 | 某些資料或必要的檢查項目缺失、不完整或未能通過。 |

請針對每項檢查項目分別進行審閱，並參照已記錄的蒐集範圍。

## 強效配置必須保留的內容

1. 在依賴資料蒐集功能之前，請透過 獨立的可信通道保留蒐集器的金鑰指紋。將該參考值與匯出檔案的簽名金鑰進行比對。
2. 請保留獨立標記時間戳記的檢查點，以及（若已使用）位於收集器管理控制範圍之外的 證人日誌。將其與 匯出的日誌進行比對，以核對其較早的邊界範圍。
3. 記錄資料擷取範圍、缺漏、篩選條件、限制及擷取過程中的變更。 針對與實際申訴相關的缺漏期間進行說明，並將未被觀察到的 訊息 ID、刪除通知及重新檢查失敗的情況明確區分。
4. 請保留原始 ZIP 檔案及其雜湊值。記錄每位持有者、轉移情況、日期 及目的。並將附有來源標示的操作員陳述與案件筆記一併保留。
5. 針對機密虛擬機器，請保留並獨立驗證引述、挑戰、 Intel 憑證鏈、測量結果、確切來源及金鑰處理條件。 請將驗證結果與已審查的證據一併保存。

See [verification scope](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope) for the checks of acquisition, archive integrity, time and collection coverage in each mode.

## 收件人審閱

請使用可信賴的 TgWitness 安裝版本，並搭配獨立取得的指紋：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

證據 ZIP 檔案必須來自獨立且可信的來源；其金鑰 及來源資訊亦須完整保留。請保留指令、工具版本、輸出結果、已審核的輸入 雜湊值以及未解決的問題。信標驗證是一項獨立的線上檢查； 報告渲染器絕不會僅為了顯示報告而聯繫任何服務。

針對特定訊息的爭議，請引用存檔參考編號、權威 檔案及紀錄參考編號，接著說明相關的時間範圍、涵蓋範圍缺口、 選取標準及佐證資料。若為共享副本，亦需檢視記錄中的 轉換過程及其對原始存檔的引用。私密篩選器與身分 映射不納入公開評估範圍。

對簽名 PDF 進行驗證可偵測受保護位元組的變更。請將原始 數位檔案與驗證結果，連同任何螢幕截圖或列印的閱讀副本一併保存。
