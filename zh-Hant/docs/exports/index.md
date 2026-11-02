# 匯出與驗證

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/

提供收件者可與收集工作區及其儲存歷史紀錄進行比對的檔案。

保留參考資料匯出已簽署的 ZIP 檔案收件者驗證

初次接觸簽名與檢查點？[試著修改一個範例記錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/concepts/#chain)，看看哪些檢查機制會偵測到此變更。

想將副本存放在收集者之外的地方嗎？請前往 [S3 設定](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3)、[Object Lock](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3-retention) 或[驗證式還原](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/#s3-restore)。

## 保留可信的參考資料

請將工作區的公鑰指紋儲存於收集器之外。在收集過程中，請將簽署過的檢查點存放在其他位置，或使用[獨立見證者](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/)。這些參考資料可讓接收者驗證金鑰及較早的日誌邊界。

## 下載已簽署的 ZIP 檔案

開啟**「匯出」**功能並建立經簽名的證據 ZIP 檔案。該檔案包含完整的作業空間日誌及經簽名的檔案清單。可使用[「報告工作室」](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reports/)製作易於閱讀的報告，或透過「[移交摘錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/handover/)」功能僅傳遞經篩選且已精簡的資料。

HTML、PDF 和 JSON 報告各自附有簽名印章，可分別進行驗證。CSV 檔是方便分析的副本；請使用經驗證 ZIP 檔內的精確 CSV 檔來檢查其完整性。若收件者同時需要原始記錄和附件，請保留該簽名 ZIP 檔。

## 請使用可信賴的 TgWitness 副本進行驗證

在已安裝的專案環境中，請替換範例中的指紋與檔案路徑：

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

當兩項參考值均通過驗證時，結果將顯示 `key_pinned: true` 和 `checkpoint_checked: true`。請將驗證結果與原始存檔一併保存。保留的檢查點必須位於匯出檔案的邊界處或之前。

## 使用驗證結果

- **請檢查交付的檔案：**清單檔案會綁定各檔案的雜湊值，而記錄簽名則會綁定已儲存的日誌。系統會偵測到檔案遭竄改或記錄鏈斷裂的情況。
- **請檢查工作區身分：**獨立保留的指紋可確認其是否為您預期的簽署金鑰。
- **比較較早的邊界：**保留的檢查點會將匯出內容與移交前儲存的日誌前綴進行比對。
- **檢視資料蒐集範圍：**缺漏處、擷取結果，以及一項受控的「傳送 → 編輯 → 刪除」測試，皆可說明此設定所擷取的事件。

請將這些結果保留於收件者的副本中。請參閱[驗證結果所確立的](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope)檢查範圍，以及對來源主張與蒐集範圍的獨立評估。

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

1. 請先向您的服務供應商建立儲存桶，然後輸入其儲存位置及憑證。在準備階段請**保持「保留異地副本**」選項未勾選，之後再選取**「儲存異地副本」**。
2. 選擇「**測試連線」**。此操作會上傳一個加密的測試物件，並檢查儲存端的回應。
3. 請選擇**「下載加密金鑰」**。請將該檔案與資料收集器分開存放；此檔案是進行資料復原的必要條件。
4. 勾選「**保留異地副本**」核取方塊，然後再次儲存。選擇「**立即複製」**以執行手動備份，或讓排程繼續運行。

## 檢查資料保留狀況與複製進度

在「**更多選項**」中，選擇保留天數，並在您的儲存桶支援「物件鎖定 (Object Lock)」時，選擇「`GOVERNANCE`」或「`COMPLIANCE`」。TgWitness 會讀取上傳物件的保留模式與截止日期。請檢視獨立的保留結果：已確認、缺少保留或檢查失敗。

控制面板會顯示上一次處理的結果、物件數量、傳輸的位元組數、已複製的日誌邊界以及任何錯誤。若發現本地儲存媒體遺失或遭變更，系統會進行通報，並於下一次處理時重新嘗試。該儲存媒體之後的檔案、檢查點及排程中的匯出項目仍可照常複製。

上傳時請使用工作區的 Direct、SOCKS5 或 HTTP 路徑。請從這些路徑中選擇其中一種進行 S3 複製；若僅選擇 MTProxy 路徑，複製作業將因錯誤而處於待處理狀態。

## 請將恢復金鑰另行存放

下載的 JSON 檔案包含解密金鑰、目標位置設定、工作區物件前綴以及簽名金鑰指紋。進行資料復原時，需同時具備此金鑰檔案以及具備儲存桶讀取權限的獨立儲存憑證。請將這些資訊納入您的復原計畫中。

若您變更了端點、儲存桶或資料夾前綴，請重新下載金鑰檔案，以確保其目標設定相符。應用程式會將本機保留的日誌、檔案及檢查點的全新副本，移至新目標位置。已完成且已從本機上傳佇列中移除的聊天記錄匯出檔，仍會保留在原有的目標位置。

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

請將復原的資料與您獨立保留的檢查點或證人記錄進行比對，然後檢視所需期間內已記錄的蒐集範圍。
