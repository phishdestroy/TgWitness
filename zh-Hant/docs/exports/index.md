# 匯出與驗證

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/

分享一份經簽署的紀錄，供他人核實。

保留參考資料匯出已簽署的 ZIP 檔案收件者驗證

初次接觸簽名與檢查點？[試著修改一個範例記錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/concepts/#chain)，看看哪些檢查機制會偵測到此變更。

想將副本存放在收集者之外的地方嗎？請前往 [S3 設定](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3)、[Object Lock](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3-retention) 或[驗證式還原](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3-restore)。

## 保留可信的參考資料

請將工作區的公鑰指紋儲存於收集器之外。在收集過程中，請將簽署過的檢查點存放在其他位置，或使用[獨立見證者](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)。這些參考資料可讓接收者驗證金鑰及較早的日誌邊界。

## 下載已簽署的 ZIP 檔案

點選「**匯出」**並建立一個經簽署的證據 ZIP 檔案。該檔案包含工作區日誌及經簽署的檔案清單。面板篩選器不會限制此完整日誌的匯出：請在分享前審閱相關內容。

獨立的 HTML 和 CSV 檔案可供下載，方便閱讀與分析。請將簽名過的 ZIP 檔案保留為可驗證的原始檔；獨立的 HTML 或 CSV 檔案並未附帶獨立的簽名。

## 請使用可信賴的 TgWitness 副本進行驗證

在已安裝的專案環境中，請替換範例中的指紋與檔案路徑：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

當兩項參考值均通過驗證時，結果將顯示 `key_pinned: true` 和 `checkpoint_checked: true`。請將驗證結果與原始存檔一併保存。保留的檢查點必須位於匯出檔案的邊界處或之前。

## 理解結果

- **完整性：**記錄的歷史紀錄與匯出的檔案均與其數位簽章相符。
- **先前觀察：**透過外部檢查點，您可以將匯出檔案與先前保留的日誌前綴進行比對。
- **實作方式：**透過「發送 → 編輯 → 刪除」的受控測試，將特定事件與擷取的記錄進行比對驗證。

有效的簽名並不能證明每則 Telegram 事件均已送達、來源所言屬實，或資料收集者的時間記錄正確無誤。

## 設定 S3 異地備份

在您的運作中工作區中，開啟**「匯出」→「異地備份」**。此選用功能支援 AWS S3 及其他相容於 S3 的服務。它會複製日誌區段、已保存的照片與檔案、附帶時間戳記回應的檢查點，以及已完成的聊天記錄匯出檔。每個物件在上傳前，都會在收集器上透過 `AES-256-GCM` 進行加密。

線上示範版本展示相同的操作介面，但已停用上傳功能。請僅在您自己正在運行的工作區中輸入儲存憑證。

[![完整的異地複製設定面板：終端點、區域、儲存桶、存取金鑰、排程、物件鎖定及復原金鑰控制](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

已展開包含進階選項的完整控制面板。畫面中未顯示任何儲存憑證。

| 領域 | 輸入內容 |
| --- | --- |
| Endpoint | 儲存服務的 URL，不含儲存桶路徑或憑證。虛構範例：`https://s3.example.invalid`。 |
| 地區 | 您的服務供應商所要求的區域代碼。應用程式的預設值為 `us-east-1`。 |
| Bucket | 一個您可存取的現有儲存桶。虛構範例：`example-case-backup`。 |
| 儲存桶中的資料夾 | 物件前綴；預設值為 `tgwitness`。應用程式會附加一個由此工作區簽名金鑰指紋衍生的前綴。 |
| 存取金鑰 ID / 秘密存取金鑰 | 請同時輸入兩組儲存憑證。這些憑證將儲存於工作區金庫中。後續儲存時，若要保留已儲存的憑證對，請將兩欄皆留空。 |
| Path 風格的網址 | 請根據服務供應商的設定，在啟用時使用 `endpoint/bucket`，或在停用時使用 `bucket.endpoint`。 |
| 複製間隔 | 範圍為 1 至 1,440 分鐘；預設為 5 分鐘。若要執行排程備份，應用程式必須處於運行狀態。 |
| Object Lock 資料保留 | 支援 Object Lock 的儲存桶之保留天數與模式。若設定為「零天」，則該儲存桶將維持預設的保留設定。 |

1. 輸入目標位置及憑證。準備期間請**保持「保留異地副本**」選項未勾選，隨後選取**「儲存異地副本」**。
2. 選擇「**測試連線」**。此操作會上傳一個加密的測試物件，並檢查儲存端的回應。
3. 請選擇**「下載加密金鑰」**。請將該檔案與資料收集器分開存放；此檔案是進行資料復原的必要條件。
4. 勾選「**保留異地副本**」核取方塊，然後再次儲存。選擇「**立即複製」**以執行手動備份，或讓排程繼續運行。

**不執行** 不會建立儲存桶。當應用程式停止運作時，排程上傳也會停止。

## 檢查資料保留狀況與複製進度

在「**更多選項**」中，請選擇保留天數，並在您的儲存桶支援 Object Lock 時選擇 `GOVERNANCE` 或 `COMPLIANCE`。TgWitness 會讀取已上傳物件的保留模式與截止日期。狀態報告會顯示確認、保留缺失或驗證失敗；僅成功上傳並不代表保留已確認。

控制面板會顯示上一次處理的結果、物件數量、傳輸的位元組數、已複製的日誌邊界以及任何錯誤。若發現本地儲存媒體遺失或遭變更，系統會進行通報，並於下一次處理時重新嘗試。該儲存媒體之後的檔案、檢查點及排程中的匯出項目仍可照常複製。

上傳資料時，系統會使用工作區的 Direct、SOCKS5 或 HTTP 路徑。透過 MTProxy 無法進行 S3 複製；該應用程式不會回退至直接連線。

**不強制** 僅因上傳請求被接受，並不代表服務提供者會強制執行「物件鎖定」（Object Lock）。

## 請將恢復金鑰另行存放

下載的 JSON 檔案包含解密金鑰、目標設定、工作區物件前綴以及簽名金鑰指紋。該檔案不包含 S3 存取憑證：還原時需另行提供具備桶（bucket）讀取權限的憑證。

若您變更了端點、儲存桶或資料夾前綴，請重新下載金鑰檔案，以確保其目標設定相符。應用程式會將本機保留的日誌、檔案及檢查點的全新副本，移至新目標位置。已完成且已從本機上傳佇列中移除的聊天記錄匯出檔，仍會保留在原有的目標位置。

**無法執行** 若未持有匯出的金鑰，則無法解密該副本。儲存空間存取憑證無法取代該金鑰。

## 在另一台機器上還原並驗證

請使用可信賴的 TgWitness 安裝版本、已下載的 JSON 金鑰、具備讀取權限的儲存空間憑證，以及一個空的輸出目錄。請替換下方虛構的憑證佔位符。

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

在驗證整個日誌、保留的檢查點以及媒體檔案的雜湊值與大小期間，下載的檔案與解密後的物件將暫存於私有臨時儲存空間中。若發現不安全的路徑、日誌段落衝突，或日誌長度短於其檢查點，系統將予以拒絕。驗證失敗時，系統不會發布任何還原的檔案。

若復原成功，系統將針對副本中的可用內容產生 `events.jsonl`、`media/`、`checkpoints/` 及 `exports/`。請將該指令的 JSON 結果與復原的內容一併保存。

**不具備以下功能**：本工具不會重建未曾記錄於日誌中的觀察結果，亦不會取代獨立保留的檢查點或證人。
