# 時間戳記

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/timestamp/

簽名檢查點的 RFC 3161 時間戳記：傳送至授權機構的內容，以及如何驗證回應。

TgWitness 會準備 RFC 3161 請求，並驗證時間戳記授權機構（TSA）的回應。 此手動程序既不會選擇 TSA，也不會提交資料；而「證據模式」則會依照 預定時程（[證據格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)）同時執行這兩項操作。已準備好的請求 **尚不**構成 **時間戳記證明**。

## 證據的約束力

流程圖 · 帳戶觀察 → SHA-256 鏈與 Ed25519 簽名; SHA-256 鏈與 Ed25519 簽名 → 簽名檢查點; 簽名檢查點 → 精確至位元的雜湊值與隨機非ce值; 精確至位元的雜湊值與隨機非ce值 → RFC 3161 請求; RFC 3161 請求 → 獨立 TSA; 獨立 TSA → 經簽署的 TSA 回應; 簽名檢查點 → 驗證資料、隨機數及明確的憑證授權機構（CA）信任關係; 經簽署的 TSA 回應 → 驗證資料、隨機數及明確的憑證授權機構（CA）信任關係 · 帳戶觀察 · SHA-256 鏈與 Ed25519簽名 · 簽名檢查點 · 精確至位元的雜湊值與隨機非ce值 · RFC 3161 請求 · 獨立 TSA · 經簽署的 TSA 回應 · 驗證資料、隨機數及明確的憑證授權機構（CA）信任關係

**圖表轉為文字**

1. 帳戶觀察 → SHA-256 鏈與 Ed25519 簽名
2. SHA-256 鏈與 Ed25519 簽名 → 簽名檢查點
3. 簽名檢查點 → 精確至位元的雜湊值與隨機非ce值
4. 精確至位元的雜湊值與隨機非ce值 → RFC 3161 請求
5. RFC 3161 請求 → 獨立 TSA
6. 獨立 TSA → 經簽署的 TSA 回應
7. 簽名檢查點 → 驗證資料、隨機數及明確的憑證授權機構（CA）信任關係
8. 經簽署的 TSA 回應 → 驗證資料、隨機數及明確的憑證授權機構（CA）信任關係

收集器的簽名將記錄與其金鑰綁定。可信的 TSA 回應可 證明某個特定檢查點在 TSA 所聲明的時間點確實存在。該 檢查點隨後可將日誌前綴與之綁定。此舉並不能證明 每項 Telegram 操作的時間，亦無法證明擷取內容的真實性。

## 操作流程

1. 請透過獨立的可信通道保留收集器的金鑰指紋。僅憑 受檢 ZIP 檔案所提供的金鑰，不足以識別該收集器。
2. 在**「匯出」→「準備時間戳記請求**」中，下載所選工作區的 請求 ZIP 檔案。解壓縮 `checkpoint.json`、`timestamp.tsq`、`SHA256SUMS` 及 `README.txt`。請勿變更檢查點位元組。
3. 選擇適合該調查的 TSA。透過其 文件中記載的方法提交 `timestamp.tsq`，並使用 `application/timestamp-query` 進行 HTTP 服務。 將原始二進位回應儲存為 `timestamp.tsr`，並記錄端點、擷取時間 及請求結果。該請求包含雜湊值與隨機數，而非訊息內容； 網路元資料仍會揭露該請求。
4. 請獨立於回覆之外取得受信任的根憑證，以及任何 所需的中間憑證。回覆中的憑證不會僅因 被包含在其中而自動成為受信任憑證。
5. 透過可信賴的 TgWitness 安裝環境，驗證：

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

如有需要，請新增 `--intermediates tsa-intermediates.pem` 或 `--openssl /path/to/openssl`。 OpenSSL 必須支援 `ts`。在 Windows 系統上，驗證器也會搜尋標準的 Git 安裝目錄。OpenSSL 3.5.9 已透過合成 CA/TSA 進行本地測試。

1. 在檢查點之後匯出經簽署的日誌 ZIP 檔案，使其包含該前綴。 請使用獨立已知的指紋進行驗證：

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. 將 ZIP 檔案、檢查點、請求、回覆、憑證鏈、驗證 結果以及交接記錄保留於收集器之外。於接收時重複進行驗證。

若要從已儲存的檢查點準備請求：

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

此準備程序會將 JSON 標準化，並將對應的檢查點納入存檔中。 請使用**該存檔中的檢查點位元組**進行 TSA 驗證，即使 輸入檔案的空白字元格式有所不同。

## 驗證範圍

| 檢查 | 當前運作方式 |
| --- | --- |
| 資料 | 檢查點字節的精確 SHA-256 值必須與回應結果相符 |
| 請求 | 透過 `--request`，原始查詢與隨機數皆會經過驗證 |
| TSA 簽名 | OpenSSL 會驗證簽名及其通往指定憑證授權機構 (CA) 的憑證鏈 |
| 收集器簽名 | 由日誌驗證器透過固定金鑰進行獨立驗證 |
| 撤銷 | 不支援自動擷取 OCSP/CRL |
| 長期有效性 | 憑證過期後將不再進行存檔驗證 |
| 排程提交 | 證據模式，預設為關閉 |

`--request` 在技術上雖屬可選，但若省略此參數，將導致無法驗證 原始隨機數。若要執行此完整程序，結果中的 `request_checked` 必須為真。 憑證驗證遵循已安裝 OpenSSL 的規則及驗證時間。 長期保存需另行制定憑證／撤銷證據政策。

有效的加密簽名並不自動等同於合格的時間戳記，亦不構成 法律上的可採納性判定。若操作員在 加註時間戳記前捏造了觀察結果，TSA 僅會將這些位元組錨定；並不能證明其真實性。

## 交接紀錄

記錄案件識別碼、發送者與收件者、UTC 傳輸時間及其來源、 目的、檔案名稱／SHA-256 值、收集器指紋、序列範圍、已知 缺口、驗證器版本及驗證結果。 請透過貴組織的流程對此 記錄進行簽署並獨立保存。TgWitness 並未 實作多使用者保管記錄系統。

開發過程中未聯繫任何獨立的即時 TSA。本地測試會建立一個 合成 CA/TSA，以檢查相容性，並驗證系統是否會拒絕已變更的資料、隨機數或 CA。
