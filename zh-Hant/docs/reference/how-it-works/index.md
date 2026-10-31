# 證據的運作方式

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/how-it-works/

文中以驗證者實際使用的精確公式，詳盡闡述了雜湊鏈、簽名、檢查點及見證者的運作原理。

TgWitness 會保存收集帳戶所觀察到的內容，將這些觀察結果 串聯成一份經簽署的日誌，並允許其他人透過可信 金鑰及先前保留的檢查點，對匯出內容進行驗證。

[本地文件網站](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally)另提供 互動式範例（網址：`/docs/concepts/`），以及檢查點決策探索工具（網址： `/docs/witness/`）。所有範例訊息、 計數及延遲皆為虛構。鏈式沙盒中的雜湊值係透過 瀏覽器中的 SHA-256 演算法計算得出。任何資料均不會傳送至 Telegram。

## 訊息隨之改變；觀察結果不斷累積

序列圖 · Telegram → 收集器: 新訊息：10:00 見面; 收集器 → 經簽署的日誌: 追加訊息.new; Telegram → 收集器: 編輯：11:00 見面; 收集器 → 經簽署的日誌: 追加訊息.已編輯; Telegram → 收集器: 刪除通知; 收集器 → 經簽署的日誌: 追加訊息.已刪除; 關於 經簽署的日誌 的說明: 原始訊息、編輯紀錄及刪除紀錄均予以保留 · Telegram · 收集器 · 經簽署的日誌 · 新訊息：10:00 見面 · 追加訊息.new · 編輯：11:00 見面 · 追加訊息.已編輯 · 刪除通知 · 追加訊息.已刪除 · 原始訊息、編輯紀錄及刪除紀錄均予以保留

**圖表轉為文字**

1. Telegram → 收集器: 新訊息：10:00 見面
2. 收集器 → 經簽署的日誌: 追加訊息.new
3. Telegram → 收集器: 編輯：11:00 見面
4. 收集器 → 經簽署的日誌: 追加訊息.已編輯
5. Telegram → 收集器: 刪除通知
6. 收集器 → 經簽署的日誌: 追加訊息.已刪除
7. 關於 經簽署的日誌 的說明: 原始訊息、編輯紀錄及刪除紀錄均予以保留

此簡化流程假設 Telegram 已成功傳送每則更新，且選定的 帳戶能夠看到該更新。操作事件也會記錄在日誌中。刪除通知 不會提供刪除者身分或確切的刪除時間。重複傳送的訊息 會被視為獨立的觀察記錄；日誌中不會進行全域性的重複資料抑制。

## 哈希值涵蓋的範圍

![觀察、編碼、雜湊與簽名：每個新事件皆包含前一個事件的雜湊值。](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

從內到外解讀此公式：**C** 將九個欄位轉換為精確的位元組； **SHA-256** 產生其摘要；**hex** 則是儲存該摘要的方式。前一個 雜湊值已包含在事件中。**unhex** 將儲存的雜湊值還原為 32 位元組，供 Ed25519 進行簽名。

[靜態鏈圖](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

設 C(ei) 為九個事件欄位的標準 UTF-8 JSON 格式。第一個 `previous_hash` 由 64 個零字元組成。每個後續記錄皆包含前一個 記錄的十六進位雜湊值：

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

該簽名涵蓋 32 位元組的原始摘要。雜湊輸入內容精確包含 `seq`、`observed_at`、`source_at`、`kind`、`chat_id`、`message_id`、`actor_id`、 `payload` 及 `previous_hash`。物件金鑰已排序；省略空白字元與 ASCII 轉義字元；NaN 與無窮大值將被排除。請參閱 [確切的編碼](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#event-canonicalization)方式。

流程圖 · 64 個零字元 → 記錄 1 / 雜湊值 h1; 記錄 1 / 雜湊值 h1 → 記錄 2 包含 h1 / hash h2; 記錄 2 包含 h1 / hash h2 → 記錄 3 包含 h2 / 雜湊 h3; 記錄 3 包含 h2 / 雜湊 h3 → 簽名檢查點：計數 3，標題 h3 (保留於其他位置) · 64 個零字元 · 記錄 1 / 雜湊值 h1 · 記錄 2 包含 h1 / hashh2 · 記錄 3 包含 h2 / 雜湊h3 · 簽名檢查點：計數3，標題 h3 · 保留於其他位置

**圖表轉為文字**

1. 64 個零字元 → 記錄 1 / 雜湊值 h1
2. 記錄 1 / 雜湊值 h1 → 記錄 2 包含 h1 / hash h2
3. 記錄 2 包含 h1 / hash h2 → 記錄 3 包含 h2 / 雜湊 h3
4. 記錄 3 包含 h2 / 雜湊 h3 → 簽名檢查點：計數 3，標題 h3 (保留於其他位置)

| 改為提供的日誌 | 偵測依據 |
| --- | --- |
| 修改記錄 2 同時保留其已儲存的雜湊值 | 重新計算的事件雜湊值有所不同；其簽名已不再涵蓋該變更後的事件 |
| 重建經竄改的記錄及其後續所有雜湊值 | 原始簽名驗證失敗；位於受影響邊界的保留檢查點結果亦不一致 |
| 移除結尾部分，但保留剩餘的前綴不變 | 在所提供的前綴之後，一個較早保留的檢查點顯示，匯出內容過短 |
| 使用另一把金鑰重新簽署替換日誌 | 透過獨立受信的金鑰指紋，可駁斥身分替換行為 |

![修改已儲存的欄位會改變其摘要；重新計算雜湊值並不會恢復原始的簽名。](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**請試著對第 2 筆記錄進行驗證：**將已儲存事件中的 `Meet at 11:00` 改為 `Meet at 12:00`。 其重新計算後的雜湊值將不再匹配。重新計算後續鏈 雖可修復其連結，但無法讓原始簽名涵蓋新的摘要。 相較之下，經觀察到的 Telegram 編輯操作，則會成為新的日誌記錄。

[靜態變更圖](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

僅憑哈希連結並無法防止他人重新計算替代鏈。 信任源自於透過獨立可信的金鑰驗證簽名， 並與儲存於收集器外部的參考資料進行比對。

## 先前檢查點新增的內容

![保留計數 3 及 h3 標題；後續匯出的 4 筆記錄將在第 3 個位置進行核對。](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**當日誌持續增長時，參考點保持不變。**若檢查點顯示 「3 筆記錄，頭部 h3」，則包含四筆記錄的匯出檔可透過匹配第 3 位置的 h3 而通過驗證。 其最新頭部為 h4，預期會有所不同。僅包含兩筆記錄的匯出檔將驗證失敗。

[靜態檢查點圖示](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

在驗證檢查點簽名後，需執行以下操作：

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

匯出資料可能跨越檢查點。其內容必須在保留的邊界處保持一致。 真正的驗證者還會檢查每個事件的順序、前一個連結、雜湊值及 簽名。若僅比較最終儲存的頭部資料，將無法察覺內部 記錄遭篡改的情況，因為其儲存的雜湊值並未隨之更新。

## 證人的歸屬之地

流程圖 · 收集器 / 帳戶會話 / 金鑰 A → 唯讀檢查點端點; Witness / 固定收集器金鑰 / 自有金鑰 B → 獨立的簽名證據日誌; Witness / 固定收集器金鑰 / 自有金鑰 B → 唯讀檢查點端點 (申請審核); 唯讀檢查點端點 → Witness / 固定收集器金鑰 / 自有金鑰 B (經簽署的回答); Witness / 固定收集器金鑰 / 自有金鑰 B → 包含經簽署的 TGW1 貼文的頻道 (Bot API / 專屬代幣) · 主機 A · 主機 B · 收集器 / 帳戶會話 / 金鑰 A · 唯讀檢查點端點 · Witness / 固定收集器金鑰 /自有金鑰 B · 獨立的簽名證據日誌 · 包含經簽署的 TGW1貼文的頻道 · 申請審核 · 經簽署的回答 · Bot API / 專屬代幣

**圖表轉為文字**

1. 收集器 / 帳戶會話 / 金鑰 A → 唯讀檢查點端點
2. Witness / 固定收集器金鑰 / 自有金鑰 B → 獨立的簽名證據日誌
3. Witness / 固定收集器金鑰 / 自有金鑰 B → 唯讀檢查點端點 (申請審核)
4. 唯讀檢查點端點 → Witness / 固定收集器金鑰 / 自有金鑰 B (經簽署的回答)
5. Witness / 固定收集器金鑰 / 自有金鑰 B → 包含經簽署的 TGW1 貼文的頻道 (Bot API / 專屬代幣)

該見證系統會記錄回滾、相同計數下的不同頭部、變更的金鑰、 無效答案及缺失的回應。僅憑計數增加，並不能證明 所有較早的記錄均未被修改；請將匯出內容與保留的 檢查點進行比對。將見證系統部署於另一台主機，可避免受收集器主機中斷的影響； 由獨立的操作員負責，則能提供額外的獨立性。

該「見證者」僅針對收集器所回報的日誌狀態進行認證，並不會 獨立監控所有 Telegram 訊息。請參閱[見證者設定說明](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/)。

## 針對已知操作進行測試

請使用受控群組、獨立的收集帳號以及新的標記。有目的地發送、 編輯及刪除訊息，並在各階段之間檢查擷取狀況。在檢視結果前，請先定義預期 的操作行為及截止條件。

R = |observed∩expected| / |expected| Δ t = treceipt - taction

僅計入與預期動作相符的項目；重複的收據不會增加 分子。分母必須不為零。若缺少收據，則無法測量 延遲。請記錄時間不確定性；請使用您自行控制的刪除動作時間， 因為 Telegram 並未提供確切的刪除時間。 例如 5/6 (83.3%) 這樣的結果描述的是測試動作，而非所有 Telegram 流量的完整性。

## 選擇工作流程

[完整的調查流程指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/investigation/)將以某起事件為例， 涵蓋頻道、群組、機器人及私人聊天室等情境：

1. 啟用「整個帳戶」調查模式，並清點所有可存取的聊天室。
2. 可取得日誌快照、各聊天室的完整歷史紀錄以及已保存的附件。
3. 將即時變更及任何有意的面板互動連同其交易憑證一併保留。
4. 透過引用的記錄及用戶檔案，追蹤數值發送者 ID、回覆關係、重複收件者及檔案 雜湊值。
5. 重建跨聊天室的時間軸，其中包含時間戳記及明確的空白處。
6. 在保持原始來源與金鑰獨立的前提下，比較其他帳戶的工作區。
7. 彙整並驗證經簽署的日誌、使用者檔案及歷史記錄匯出檔，並附上案件筆記。

該網站的《`/docs/cases/`指南》包含互動式案件地圖，並針對 機器人爭議、已刪除訊息及參與者更名等情況提供多種處理方案。案件筆記 與跨工作區分析屬外部功能；本應用程式不會自動 生成全球調查圖譜或合併案件檔案庫。

[已完成驗證與待完成工作](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/) · [匯出與驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#investigation-handoff) · [從一個帳戶開始](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/quickstart/)
