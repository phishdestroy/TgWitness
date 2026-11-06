# 獨立見證人

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/

請使用具備專屬金鑰與機器人的「Witness」執行程序，將簽署過的檢查點發佈至頻道，並據此核對匯出資料。

[匯出與驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/) · [高可信度](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/) · [面板指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

流程圖 · 收集器 → Witness (簽名檢查點：記錄數 + 頭部雜湊值); Witness → Witness 日誌，自有金鑰; Witness → Telegram 頻道 (透過其自有機器人發布的簽名貼文); 證據 ZIP 檔案 → verify.py; Witness 日誌，自有金鑰 → verify.py; Telegram 頻道 → verify.py (Telegram 桌面版匯出功能或 t.me/s 頁面) · 收集器 · Witness · Witness 日誌，自有金鑰 · Telegram 頻道 · 證據 ZIP 檔案 · verify.py · 簽名檢查點：記錄數 + · 頭部雜湊值 · 透過其自有機器人發布的簽名貼 · 文 · Telegram 桌面版匯出功能或 · t.me/s 頁面

**圖表轉為文字**

1. 收集器 → Witness (簽名檢查點：記錄數 + 頭部雜湊值)
2. Witness → Witness 日誌，自有金鑰
3. Witness → Telegram 頻道 (透過其自有機器人發布的簽名貼文)
4. 證據 ZIP 檔案 → verify.py
5. Witness 日誌，自有金鑰 → verify.py
6. Telegram 頻道 → verify.py (Telegram 桌面版匯出功能或 t.me/s 頁面)

## TgWitness 能提供什麼，以及它無法提供什麼

| 該證據日誌具備 | 該證人從未 |
| --- | --- |
| 適用於單一工作區的唯讀**見證代幣** | 資料收集者的 Telegram 會話或 API 憑證 |
| 其專屬的 Ed25519 金鑰與日誌 | 收集器的儲存庫、簽名金鑰或面板憑證 |
| 專屬的 Telegram 機器人代幣 | 訊息內容：開頭為記錄數量及雜湊值 |

該憑證是在**「Extras」→「Independent witness」**中建立的，僅顯示一次，且僅以 SHA-256 的形式儲存。它會開啟一個且僅一個端點， `GET /api/witness/head`，該端點會回傳一個剛 簽署的檢查點，以及經簽署的無內容集合計數器和運作狀態。 它無法開啟面板、讀取訊息內容或變更設定，且 該處不接受面板代幣。請在同一頁面撤銷代幣。收集器會記錄 新見證金鑰開始檢查的時間（`witness.seen`) 並顯示每個令牌的最後一次檢查時間； 若見證者在 2.5 個間隔內未進行檢查，則會被標記為逾期。

新見證者會在 每次投票時發送一個隨機挑戰；擷取陳述會於收集器簽名下方重複該挑戰。計數器 與確切的檢查點綁定，並包含在簽名的見證貼文中。舊版見證者 仍可被獨立見證者接受。僅日誌的增長絕不會被計為新訊息。

## 其檢查與記錄的內容

每隔一段時間（預設為 10 分鐘），Witness 會：

1. 自行擷取頭部資料（收集器無法推送或跳過該部分）；
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
3. 將一份經簽署的記錄附加至其自身的日誌中：`witness.anchor`，狀態為 `ok`、 `key_changed`、`rollback`（記錄數量少於先前）、`fork`（長度相同，但 標頭不同）或 `invalid`（回應未能通過驗證），或當 收集器未回應時為 `witness.no_response`；
4. 將結果發佈至頻道，並附有簽名，包含「無回應」的情況，只要 TgWitness 正在運行且能連線至 Bot API。發佈 ID 已記錄（`witness.posted`）， 發佈失敗的情況亦同（`witness.post_failed`）。

一則貼文的樣貌如下；最後一行載有經簽署的聲明：

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## 執行 TgWitness

您需要一個 Telegram 機器人（可透過 @BotFather 建立），一個由該機器人擔任 管理員的頻道，以及一個可從證人端存取的收集器位址——需透過 HTTPS 連線，且位於 私有網路之外（請參閱[部署](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/)章節中的 HTTPS 設定檔）。

在面板中開啟**「附加功能」→「獨立見證人」→「設定」**。三個步驟涵蓋 唯讀存取權限、您的頻道與間隔時間，接著啟動見證人。發佈 政策、可選用的 HTTP/SOCKS5 代理伺服器以及自訂 Bot API 位址皆位於**「進階設定」**中。此表單 會下載 `witness.json` 時，會預先填入此工作區的收集器金鑰。請透過「**將存取檔案儲存**為」功能下載新 建立的唯讀憑證 `witness-token.txt`」下載新建立的唯讀憑證；將其與 `bot-token.txt`在見證主機上建立的檔案，一併放置於該 JSON 檔案旁。收集器絕不會接收機器人憑證。 下載過程不會啟動任何服務，也不會發佈任何訊息。任何託管專案的見證者均不會 被隱含地註冊。

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

第一個指令會檢查配置檔和密鑰檔案，過程中不會發出網路請求或建立金鑰。 JSON 中的路徑是以該檔案為基準的相對路徑；CLI／環境路徑則是以 工作目錄為基準的相對路徑。 將見證者的指紋保留在其主機之外。收集器的 「最後輪詢」指標僅用於確認請求；發布狀況則由 Proof 回報，或可透過 見證者日誌及頻道進行查核。

若控制面板位於 SSH 隧道後方，請參照此[Caddy 範例](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example)，僅在 獨立的 HTTPS 主機名稱上公開範圍限定的 Witness 端點。 預設工作區將使用 `https://witness.example.org`，其他工作區則使用 `https://witness.example.org/profiles/ID`。仍需提供存取憑證；該虛擬主機不會轉發控制面板及其 其他 API 路由。

選擇 `all` 以獲取定期發布的檢查點。五分鐘的間隔意味著每個工作區每天約有 288 則貼文。`changes`/`problems` 會刻意不發布部分檢查點。 MTProxy 適用於資料收集者的 Telegram 客戶端。Witness 的 HTTP 輪詢與 Telegram 的 HTTPS Bot API 會使用各自的直接連線／HTTP／SOCKS5 路由（[Bot API](https://core.telegram.org/bots/api)）。

**在收集器旁邊，使用 Docker**（同一主機——獨立的程序和金鑰，但 由同一位操作員管理）：將數值填入 `.env` 並啟動該設定檔。

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

若使用已發布的圖片，請標註 `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`。

**若部署於他人伺服器**（真正的獨立見證者）：將儲存庫複製至該處，將 `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` 以及上述三個數值 設定至 `.env`，然後

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

或不使用 Docker：

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### 發佈至 Discord

見證者可選擇在 Discord 頻道而非 Telegram 上發文。在 Discord 中，開啟 **「編輯頻道」→「整合」→「Webhook」**，建立一個 Webhook 並複製其網址。在 設定面板中，於步驟 2 選擇**「Discord Webhook · 您的頻道」**。在見證者主機上， 將該網址儲存為 `discord-webhook.txt` 旁 `witness.json`；該連結絕不會傳送至 收集器。

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

每位見證者僅有一位發布者：Telegram 頻道或 Discord Webhook，不可同時具備兩者。貼文 均包含相同的簽名聲明，且無法標記任何人。若貼文長度超過 Discord 的 2,000 個字元，則會被一行簡短文字取代，並附上完整的檢查碼作為 `witness-check.txt`。每則貼文的 ID 會以 `witness.posted`. `verify.py --channel`僅讀取 Telegram 頻道的匯出資料，因此針對 Discord 請保留見證日誌：其中包含 每筆檢查紀錄。

### 選項

| 選項 | 環境 | 預設 | 含義 |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | 檢查間隔時間，1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | 等待資料收集器與 Bot API 的時間為 5 至 600 秒 |
| `--post` | `_POST` | `all` | `all`：每項檢查；`changes`：新進展或新問題；`problems`：盡是問題與未解之謎 |
| `--title` | `_TITLE` | `TgWitness witness` | 每個頻道貼文的開頭字句 |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | 請將收集器金鑰固定，而非直接採信第一個答案 |
| `--proxy` | `_PROXY` | 直接 | `socks5://host:port` 或 `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Bot API 位址，例如本地的 Bot API 伺服器 |
| `--data-dir` | `_DATA` | `witness-data` | Witness 金鑰與日誌 |
| `--config` | `_CONFIG` | – | 包含上述任一選項的 JSON 檔案 |

收集器的地址、代幣及頻道來自 `--collector`, `--token` 或 `--token-file`, `--bot-token` 或 `--bot-token-file`, `--discord-webhook-file` 以及 `--channel`， 或 `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` 以及 `_CHANNEL`，這能防止機密項目出現在程序清單中。

配置檔採用帶有底線的選項名稱，並加上`texts`，該代碼會替換頻道貼文中的 文字：

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts` 金鑰：`ok`、`key_changed`、`rollback`、`fork`、`invalid`、`no_response`、`collector`、 `records`、`head`。命令列優先於環境變數，環境變數優先於檔案。 未知選項或文字金鑰會觸發警告訊息並中止記錄，而非被忽略。 文字表述絕不影響驗證：verify.py 會在每次 發文結束時檢查簽名代幣。 在 `--post changes` 或 `problems` 中，未發布的檢查仍會保留在 見證日誌中，而 `verify.py` 會將其標示為「從未發布」；起始記錄會標明 相關政策。每項檢查仍會出現在日誌中，因此發布次數減少僅意味著獨立的 Telegram 傳送次數減少，而非檢查數量減少。

即使沒有頻道，Witness 仍會持續維護其日誌。請將 Witness 金鑰指紋 (`python -m tgwitness.witness fingerprint`) 存放在其他地方。

## 多個工作區的公開驗證頁面

`python -m tgwitness.proof` TgWitness 最多可同時監控 32 個工作區，並提供一個唯讀 頁面，顯示每個工作區最新的簽名檢查結果。每個工作區在 data 資料夾下都有專屬的見證金鑰和 日誌，以及一個固定收藏金鑰；是否發佈至 Telegram 頻道 則可針對每個工作區自行選擇。請從 [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example) 開始：

| 領域 | 含義 |
| --- | --- |
| `title` | 頁面標題，1–100 個字元 |
| `data_dir` | 與檔案相關的 Witness 金鑰和日誌；預設值 `proof-data` |
| `interval`, `timeout` | 檢查間隔（分鐘，範圍 1–1440，預設值 5）；等待時間（秒，範圍 5–600，預設值 20） |
| `workspaces[].id`, `label` | 簡短的小寫別名與顯示名稱 |
| `workspaces[].collector` | 收集器地址；其他工作區的結尾為 `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | 必備項目，每個工作區各不相同 |
| `workspaces[].token_file` | 包含該工作區唯讀見證代幣的檔案 |
| `workspaces[].channel`, `bot_token_file` | 可選功能：將每次檢查結果發佈至頻道 |
| `workspaces[].proxy`, `bot_api` | 可選的路徑與 Bot API 位址 |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

第一個指令會在不建立連線的情況下，驗證檔案及代幣檔案。 該頁面僅回應 GET 和 HEAD 請求：

- `/` 顯示所有工作區；若某個工作區在 2.5 個間隔內未被檢查，則會被標記為過期。
- `/api/proof` 回傳的結果與 JSON 相同。
- `/api/proof/<id>` 下載最新的簽署聲明（`tgwitness-public-proof-v1`)： 見證記錄編號與雜湊值、狀態、固定收藏器金鑰、檢查點、收集 計數器，以及頻道發文是否成功，並由該工作區的見證金鑰簽署。
- `/healthz` 當工作區的監控程式停止運作時，會回傳 503 錯誤。

請為該頁面設定專屬的主機名稱，例如 [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example)。為進行驗證，請使用 以下說明中的方法匯出 工作區的見證日誌， `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` ，並依照 以下說明使用該日誌。

## 驗證

在「witness」端，匯出其日誌：

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

接著，無論身在何處，只要擁有收集器產生的簽名 ZIP 檔案，以及從 Telegram Desktop 匯出的頻道（*「匯出聊天記錄* 」→「JSON」會產生 `result.json` ）或其公開的 `https://t.me/s/…` 頁面：

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` 會檢查證人日誌（鏈與簽名），接著確認**證人 所見的每個頭部皆屬於匯出日誌的一部分**：該計數處的記錄必須擁有精確 對應的雜湊值。若頭部不匹配，則驗證失敗——表示日誌在 證人查看後遭到篡改。 它還會報告匯出後所見的頭部記錄、見證人 記錄的異常情況、驗證失敗的回應、其匹配檢查點存在於此 匯出檔中的時間段（「見證範圍從 X 至 Y」），以及缺口。後續的檢查點不會延長這些時間段。 結果包含最後一個匹配的記錄編號，以及後續 未找到匹配檢查點的記錄數量。僅計入由該匯出檔自身金鑰簽署的回答：若匯出檔 由見證者從未見過的金鑰簽署，則會被報告為「未見證」；若未採用`--fingerprint`，其 簽署者將保持未錨定狀態。 採用 `--channel` 時，每個簽署的貼文都必須與見證日誌 逐筆匹配：已變更的貼文將驗證失敗，缺失的貼文則會被列出。在 提供的 Telegram JSON 匯出檔中，日期屬於可編輯的元資料，不屬於簽署的見證代幣範圍。 代幣匹配並不能驗證發布日期；結果會明確 報告未執行發布時間的驗證。

### 需設定經見證的匯出範圍

若需進行必須包含經見證之最終紀錄的交接，請加入 `--require-witness`：

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

這需要獨立保留的「見證者指紋」以及與此匯出檔案 精確末尾相符的檢查點。僅涵蓋較早前前綴的檢查點 是不夠的。請暫停收集，讓見證者觀察最終狀態，並在 進一步寫入日誌之前進行匯出；若日誌發生變更，請保留另一個檢查點並 匯出該狀態。 僅憑後續的檢查點無法驗證較短匯出檔的最終雜湊值。 當同時提供 `--channel` 時，若聲稱的貼文缺失或匹配集為空，將導致此 嚴格檢查失敗。若未啟用此標誌，一般完整性檢查仍會報告未經見證的 記錄，但不會因此拒絕一個在其他方面完整的存檔。

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.
