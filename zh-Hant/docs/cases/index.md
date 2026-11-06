# 跨所有聊天室進行調查

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/cases/

一個橫跨頻道、群組、私人聊天和機器人的完整案件：收集、串連線索、重建時間軸、移交。

一個虛構事件，從頭到尾。收集、搜尋和人員檔案找出紀錄，[Case Board](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/case-board/) 整理它們，[Report studio](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reports/) 呈現它們。

已處理案例／付款目的地變更

### 一樁事件。四段對話。一條待重構的軌跡。

一則頻道貼文指向一個機器人。一個群組在討論新的付款連結，機器人也顯示了它。貼文被編輯，私人聊天重複了這個連結，一則群組訊息消失了。

每一個版本是由誰發布的？該連結出現在哪裡？哪個檔案被保留下來了？有哪些變更，以及何時進行的？

歷史載入、AI、MCP、OCR 和 webhook：[運用檔案庫](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/archive/)。

## 1. 建立涵蓋整個帳戶的記錄範圍

整個帳戶範圍只用於專用帳戶。主帳戶只用選定的聊天室或一個資料夾。

1. 在獨立工作區中[連接帳戶](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/accounts/)。記下案件編號、帳戶 ID、工作區和金鑰指紋。
2. **來源 → 觀察範圍 → 調查模式**：**整個帳戶**、全部四種來源類型、**自身操作**。每個新聊天室都會保存其資料和最近 **200 則可見訊息**。按**儲存範圍**並確認。
3. **載入對話**並與帳戶的聊天清單比較。上限為 1,000 個對話（在**參數 → 從帳戶清單讀取的聊天室**中最多可設為 20,000）；超出上限的聊天室在變得活躍後才會出現。
4. **記錄設定** → **所有可見活動**，檢查附件限制和磁碟空間。啟動後，用一則訊息、一次編輯和一次刪除來測試。

頻道群組私人聊天室機器人

一個帳戶／一個簽署金鑰**所有選定的、帳戶可見的活動 → 整合為一份日誌**

訊息 · 編輯 · 刪除通知 · 可見反應 · 群組活動 · 自身操作

「整個帳戶」是指此帳戶能開啟的每個聊天室，扣除排除項目。不含祕密聊天。新聊天室出現時即加入；舊歷史不會自動下載。

## 2. 取得歷史紀錄並保存檔案

建立一個 Case Board 集合，將重要內容加入書籤。維護一份來源登記表：聊天室 ID、標題、帳戶、角色、即時擷取開始時間、歷史結果、媒體結果、空缺。

| 需求 | 面板中的操作 | 功能介紹 |
| --- | --- | --- |
| 已啟用聊天室的歷史紀錄 | 來源 → 載入完整歷史紀錄 | 可用的過往訊息會進入工作區日誌，並具備暫停／恢復功能及經簽署的進度報告。[歷史紀錄指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/history/)。 |
| 日誌中的現有聊天內容 | 來源 → 記錄設定 → 歷史快照 | 最近的訊息作為簽名紀錄。預設 500 則，在**參數 → 最大歷史快照**中最多可設為 10,000。 |
| 某個聊天室目前可見的完整歷史紀錄 | 完整聊天記錄匯出 → 匯出完整聊天記錄，或 聊天 → 匯出聊天記錄 | 每個聊天室一個獨立的簽名包，含 `chat.json` 和 `chat.html`。 |
| 當出現新聊天室時的背景說明 | 監測範圍 → 當出現新的聊天室或機器人時 | 它的資料和最多 1,000 則最近訊息（調查模式下為 200 則）。不套用於既有聊天室。 |
| 附件位元組 | 下載可見附件 + 各類別上限 | 尋找附 SHA-256 和大小的 `media.saved`。排隊中、已略過或失敗都代表未保存。 |

聊天匯出不會進入日誌或人員檔案。若要在 TgWitness 內搜尋舊歷史，請使用**載入完整歷史紀錄**或快照。

這裡是：頻道、群組、機器人聊天和私人聊天，以及發票檔案及其雜湊。擷取前已刪除的內容已經不在了。

## 3. 記錄不斷演變的對話內容以及您自身的行動

保持執行。將熱門聊天室加星號作為優先，在**記錄設定 → 重新檢查**中調整重新檢查，並留意 `recheck.completed`、FloodWait 和媒體結果。

**聊天室 → 個人資料 → 立即儲存個人資料**會保存聊天室的簡介、機器人指令和其他中繼資料。

**作為案件調查的一部分，追蹤機器人或接受邀請**

1. **聊天室 → 開啟 Telegram 連結**，先儲存預覽。連結和預覽會成為簽名紀錄。
2. 如有需要，**加入 / 開啟並觀察**會加入聊天室，或以啟動參數啟動機器人。
3. 若要記錄某個動作，請在面板中回覆或使用**按下按鈕**。您會得到 `interaction.requested` 和 `interaction.result` 以及機器人的回答。

這些是真實動作。在其他應用程式中按下的按鈕看不到，只看得到機器人的回覆。不支援網頁應用程式、付款或電話/位置。

## 4. 追蹤聊天室中的人員、連結與檔案

1. **日誌**、**所有來源**，搜尋片語、網域或使用者名稱。開啟結果並**新增至案板**。
2. **聊天室 → 人員 → 開啟個人檔案**，選擇一個人：名稱歷史、回覆、活動、**也出現在…**、連結、錢包、電話。開啟被引用的紀錄。
3. 在其他聊天室追蹤同一個數字使用者 ID。相同的名稱、錢包或大頭貼只是線索，不是證據。
4. 比較檔案雜湊。SHA-256 相同 = 位元組相同。是誰分享的則是另一個問題。

案例地圖 / 追蹤參考資料虛構案例 · 非即時圖表

頻道 / 公告**原文 → 編輯後內容**

記錄 #101、#188 訊息 #84 · 未標示發送者

群組 / 運作**使用者 71001 發布了新連結**

記錄 #146 · 訊息 #309 已儲存檔案收據 #151

BOT / 訂購對話**一個按鈕可導向該頁面**

記錄 #173 · 訊息 #12 返回按鈕的元資料

私密 / 後續追蹤**使用者 71001 重複輸入目的地**

記錄 #205 · 訊息 #922 已儲存檔案收據 #209

四個聊天室提供了不同的觀察結果。請追蹤每項連結的原始記錄；該頻道貼文並未標示發送者。

本操作指南中的數字 ID 和記錄參考編號均為虛構。此說明圖示範了如何將搜尋結果、個人檔案與已檢視的記錄相互關聯；「案件看板」則儲存對應的卡片及來源參考資訊。

| 連結 | 輔助觀察 | 結論：保留 |
| --- | --- | --- |
| 同一 Telegram 帳號 | 群組 #146 及私人聊天室 #205 中的使用者 ID 71001 | 兩個聊天室中的傳送者 ID 相同。這個人在現實中是誰是另一個問題。 |
| 重複的目標 | `pay.example.invalid/new` 在 #146、按鈕元資料 #173、編輯過的貼文 #188 及 #205 | 同一個連結出現在四個地方。誰控制它需要其他來源。 |
| 相同檔案位元組 | 已完成的媒體收據 #151 和 #209 中的 SHA-256 值完全相同 | 兩個檔案逐位元組相同。 |

檔案只涵蓋在*此工作區*中發過言的人，不是成員清單。每項事實的引用數：**參數 → 每項事實引用的紀錄**。

## 5. 重建事件序列並標記缺漏處

先在**聊天室**中查看版本，再到**日誌**中選擇**所有來源** + **編輯**、**刪除**、**涵蓋範圍**。時間軸上寫下兩個時間：Telegram 的日期和被觀察到的時間。

1. 09:00 · #101**已擷取的頻道貼文**

   原始目標網址已保留。
2. 09:12 · #146 / #151**群組提供了一個不同的連結**

   使用者 71001 發佈此內容；附件下載完成。
3. 09:16 · #173**該機器人顯示相同的目的地**

   儲存的鍵盤元資料中包含該連結。
4. 09:20 · #188**頻道公告變更**

   原始內容與編輯後的內容均予以保留。
5. 09:24 · #205 / #209**私人後續訊息再次重申此點**

   所儲存的附件與 #151 具有相同的完整 SHA-256 值。
6. 09:28 · #231**群組刪除通知已送達**

   先前的觀察依然成立：系統既未提供刪除者身分，也未提供確切的刪除時間。

示例中的觀察時間與參考資料。其他日誌記錄則位於這些條目之間。

日誌順序是抵達順序，不一定是發生順序。請將即時紀錄、快照、復原的訊息、刪除和「重新檢查時缺少」分開，並將每個空缺標記為未知。

## 6. 將此案例擴展至其他資料蒐集帳戶

每個帳戶一個工作區，步驟相同。記下每個帳戶的角色和指紋。訊息編號依帳戶計算，所以務必註明是哪個工作區和聊天室。

[帳戶群組](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/groups/)顯示狀態、共用設定並一起匯出所有帳戶，每個帳戶仍有自己的日誌和金鑰。跨帳戶時間軸需要您在筆記中自行整理。

案件時間很長？請加入[獨立見證人](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)，並測試每個帳戶實際捕捉到什麼。

## 7. 交付可核查的案件資料包

每個工作區的簽名 ZIP（一律是完整日誌，篩選不影響），以及人員檔案、聊天匯出和檔案。

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

請另外傳送指紋。每份都對照它自己的工作區驗證：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

將驗證工具的輸出、原始檔案、涵蓋範圍和移交紀錄與您的發現放在一起。在 Report studio 中撰寫報告。若接收方需要的更少，請製作[精簡移交](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/handover/)。
