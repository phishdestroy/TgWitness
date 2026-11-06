# 匯出與驗證

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/

交給對方能自行對照您的工作區核對的檔案。

保留參考資料匯出已簽署的 ZIP 檔案收件者驗證

不熟悉簽名和檢查點？[修改一筆範例紀錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/concepts/#chain)，看看哪項檢查會發現它。

想將副本存放在收集者之外的地方嗎？請前往 [S3 設定](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3)、[Object Lock](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3-retention) 或[驗證式還原](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3-restore)。

## 保留可信的參考資料

請把工作區金鑰指紋記在收集器以外的地方。收集期間，也請將簽名檢查點存放在別處，或執行[獨立見證人](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)。接收方正是用這些來核對金鑰和日誌的早期狀態。

## 下載已簽署的 ZIP 檔案

**匯出** → 簽名證據 ZIP。其中包含完整日誌和簽名檔案清單。可在 [Report studio](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reports/) 中製作易讀的報告，或只將選定資料作為[移交擷取](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/handover/)傳送。

HTML、PDF 和 JSON 報告帶有各自的封印。CSV 只是工作副本；若需完整性，請使用已驗證 ZIP 內的 CSV。

## 請使用可信賴的 TgWitness 副本進行驗證

在專案環境中，使用您自己的指紋和路徑：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

通過時會顯示 `key_pinned: true` 和 `checkpoint_checked: true`。請將該輸出與封存檔放在一起。檢查點必須位於匯出結尾或之前。

## 使用驗證結果

- **檔案：**清單綁定它們的雜湊，簽名綁定日誌。任何變更都會顯現。
- **身分：**您保存的指紋證明這就是您預期的金鑰。
- **早期狀態：**檢查點將匯出與移交前保存的日誌前綴進行比較。
- **涵蓋範圍：**空缺、擷取結果以及「傳送 → 編輯 → 刪除」測試，顯示這套設定實際捕捉到什麼。

詳細資訊：[驗證能證明什麼、不能證明什麼](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope)。

## 設定 S3 異地備份

在工作區中開啟**匯出 → 異地副本**。支援 AWS S3 以及任何相容 S3 的儲存空間。它會複製日誌區段、已儲存的檔案、附時間戳記的檢查點和已完成的聊天匯出，每一項在離開收集器之前都以 `AES-256-GCM` 加密。

線上展示版會顯示這些控制項，但上傳已關閉。請只在您自己的安裝中輸入真實憑證。

[![完整的異地複製設定面板：終端點、區域、儲存桶、存取金鑰、排程、物件鎖定及復原金鑰控制](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

已展開包含進階選項的完整控制面板。畫面中未顯示任何儲存憑證。

| 領域 | 輸入內容 |
| --- | --- |
| Endpoint | 儲存空間 URL，不含 bucket 路徑或憑證。範例：`https://s3.example.invalid`。 |
| 地區 | 依服務商要求填寫。預設 `us-east-1`。 |
| Bucket | 一個您有寫入權限的現有 bucket。範例：`example-case-backup`。 |
| 儲存桶中的資料夾 | 前綴，預設 `tgwitness`。其上還會加上每個工作區的前綴。 |
| 存取金鑰 ID / 秘密存取金鑰 | 兩者一起填寫，儲存在金庫中。之後兩者都留空即可保留原值。 |
| Path 風格的網址 | 開啟：`endpoint/bucket`。關閉：`bucket.endpoint`。視服務商而定。 |
| 複製間隔 | 1 至 1,440 分鐘，預設 5。僅在應用程式執行時有效。 |
| Object Lock 資料保留 | 天數和模式，前提是 bucket 支援 Object Lock。填 0 則保留 bucket 預設值。 |

1. 建立 bucket，在不勾選**保留異地副本**的情況下填寫目的地和憑證，按**儲存異地副本**。
2. **測試連線**會上傳一個加密的測試物件。
3. **下載加密金鑰**，並存放在遠離收集器的地方。沒有金鑰就無法復原。
4. 勾選**保留異地副本**，儲存，然後**立即複製**，或讓排程執行。

## 檢查資料保留狀況與複製進度

在**更多選項**中選擇保留天數以及 `GOVERNANCE` 或 `COMPLIANCE`。TgWitness 會從已上傳的物件讀回保留設定並告訴您：已確認、缺少或檢查失敗。

面板顯示上一輪、物件數量、位元組、已複製的日誌邊界和錯誤。遺失的本機檔案會被回報並在下一輪重試，其餘內容繼續複製。

上傳可走直接連線、SOCKS5 或 HTTP。若路由只有 MTProxy，副本會帶著錯誤等待。

## 請將恢復金鑰另行存放

金鑰 JSON 包含解密金鑰、目的地、前綴和金鑰指紋。復原時需要它以及具讀取權限的儲存空間憑證。

變更了端點、bucket 或前綴？請重新下載金鑰。新的副本會從新目的地開始；舊的聊天匯出留在原處。

## 在另一台機器上還原並驗證

您需要一個可信任的 TgWitness 安裝、金鑰 JSON、唯讀儲存空間憑證和一個空資料夾：

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

所有內容會先在私人暫存資料夾中檢查：完整日誌、檢查點、檔案雜湊和大小。不安全的路徑、互相衝突的區段，或比其檢查點更短的日誌都會導致失敗，此時不會寫出任何內容。

成功後您會得到 `events.jsonl`、`media/`、`checkpoints/` 和 `exports/`。請將指令的 JSON 輸出與它們放在一起，並與您自己保存的檢查點或見證紀錄比較。
