# Telegram · 儲存與還原

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/storage/

備份功能、將舊檔案移至您的雲端儲存空間、在 Object Lock 下的副本，以及在新裝置上的資料恢復。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [部署與復原](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/)

![部署與復原](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

該面板將任務分為三類：

| 任務 | 功能說明 |
| --- | --- |
| 保留備份 | 將已簽名的日誌、檢查點、備份檔案及排程中的匯出項目複製到已設定的 S3 儲存位置。 |
| 免費的本地儲存空間 | 將選定的舊附件複製到 S3 或 rclone 雲端遠端儲存空間，完整讀回內容，驗證加密位元組，然後刪除已驗證的本地副本。 |
| 保留一份證據副本 | 設定 S3 Object Lock 並檢查回傳的保留狀態。該服務必須確認所請求的模式與日期。 |

釋放儲存空間時，絕不會刪除或覆寫已簽名的日誌。每個附件均保留 其原始 SHA-256 以及一份恢復憑證。可選的 gzip 壓縮會在 經過驗證的加密之前進行。雲端檔案名稱不包含 Telegram 名稱、 聊天 ID 或原始附件名稱。單一附件最大可達 32 GiB。

僅憑上傳回應並不能作為刪除檔案的授權。TgWitness 會下載 完整的加密物件並驗證其大小，SHA-256 則會儲存收據， 並在刪除前立即再次檢查本機的位元組數。若發生上傳失敗、 讀回結果不符或傳輸被取消的情況，本機檔案將保留原狀。若 已啟用的證據備份尚未複製該檔案，刪除操作亦會等待備份完成。

**本頁內容**

- [當磁碟空間即將用盡時](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/storage/#when-the-disk-is-filling-up)
- [連接目標位置](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/storage/#connect-a-destination)
- [保留還原檔案](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/storage/#keep-the-recovery-file)
- [安裝資料遺失後的恢復步驟](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/storage/#recover-after-losing-the-installation)
- [操作員機器人與完成通知](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/storage/#operator-bot-and-completion-notices)

## 磁碟空間即將耗盡時

當可用空間低於**參數 → 附件 → 可用磁碟空間**中的門檻（預設 1 GiB）時，附件下載會暫停並保留佇列。文字觀察繼續進行。這不受通知設定影響：關閉通知不會關閉下載預留空間或儲存保護措施。

若要提早介入，請啟用**自動執行**，選擇**刪除本機檔案以釋放空間**，並啟用**磁碟空間不足時額外執行一次轉存**。此選用規則預設在可用空間低於 5120 MiB 時啟動，分批處理直到可用空間達到 10240 MiB。兩個門檻皆可設定。它與手動執行使用相同的目的地、檔案最短存放時間、批次上限、完整回讀驗證及證據備份前提條件，不會自行啟用目的地。每 30 秒檢查一次；發生錯誤或沒有進展時，下次嘗試延後五分鐘。規則狀態及重試時間在重新啟動後保留。規則未啟動時，排程工作仍依正常間隔執行。

面板顯示可用空間、封裝預留空間、空間不足規則是否就緒，以及因暫存空間不足而略過的檔案。封裝和還原在開始前檢查暫存空間的峰值需求，並在寫入期間檢查可用空間。預留量使用下載設定，但儲存操作至少保留 64 MiB。這些檢查不是檔案系統配額；其他程序仍可能在兩次檢查之間耗用空間。

Gzip 對遠端物件進行無損壓縮，不會縮小使用中的日誌，也不會建立本機封存檔。JPEG、影片及 ZIP 可能幾乎不縮小，甚至略微增大。啟用壓縮時，目前封裝流程可能暫時需要約兩倍附件大小的空間，再加上預留量。請為最大的檔案選擇足夠早的啟動門檻。無法封裝的過大檔案會保留並回報；較小檔案及已驗證的遠端副本仍可釋放空間。已有驗證通過的副本時，不必再建立本機封裝檔即可移除本機檔案。還原也需要暫存空間，空間不足時可能遭拒。

沒有符合條件的可移動檔案或未設定目的地時，TgWitness 無法自動回收空間。儲存管理絕不會裁剪或重寫簽署過的日誌。新的文字觀察仍需要磁碟空間。

## 連接目標位置

在**「附加功能」→「儲存空間與磁碟空間」→「管理儲存空間**」中，選擇任務與目標位置， 儲存後，再選取「**測試上傳與下載**」。此測試會上傳一個隨機的小型探測資料，並將其 讀回。此過程不會使用 Telegram 的內容。

若使用 S3，請採用服務供應商的實際端點、區域及儲存桶。Wasabi、Backblaze、 Cloudflare R2 及其他相容服務均採用相同的 S3 設定。僅具備相容 API 並不代表支援 Object Lock。在「治理模式」下， 經授權的管理員可能繞過保留設定；而「合規模式」則有不同的 限制。在依賴保留設定之前，請先查閱回傳的 Object Lock 狀態。

若要設定 rclone 目標位置，請透過 rclone 的提供者設定建立一個遠端，並 將該遠端的 `[name]` 區段貼入面板中。已安裝的輔助程式支援 MEGA、Google Drive、OneDrive、Dropbox、Box、pCloud 以及 選取器中顯示的其他服務提供者。憑證會儲存於此工作區的加密保管庫中。OAuth 授權更新資訊會儲存回保管庫。憑證不會新增至日誌 事件，也不會包含在還原下載檔案中。

此輔助程式安裝於工作區內，並附有固定版本及 SHA-256。 它不會被加入系統 PATH。設定檔和工作檔是 該工作區內的暫存檔。基於命令列及本機檔案的遠端連線將被 拒絕。rclone 目前要求針對 外部請求明確選取**「Direct」**路由。若工作區採用 SOCKS5 或 HTTP 路由，請使用原生 S3 儲存空間； rclone 不會在路由不可用時靜默繞過。

## 請保留還原檔案

請選擇「複製檔案後**儲存還原檔案**」，並將其存放於 安裝目錄以外的位置。該檔案包含解密金鑰及已簽署的物件 收據，因此請將其視為私鑰備份。請同時將原始的遠端設定 及目標憑證分開存放。在後續複製操作之前所建立的 還原檔案，將不包含該後續檔案的收據。

簽名金鑰的指紋應已獨立記錄在案。若僅 依據同一檔案內提供的金鑰來驗證簽名，並無法確定該 還原檔案的歸屬。

若要修復現有工作區中遺失的儲存收據，請開啟**「從已儲存的還原檔案還原檔案**」， 並選取該檔案。該面板會驗證簽名，並要求使用相同的工作區 簽署金鑰。若儲存金鑰不同，系統將拒絕進行替換。接著選擇**「還原 所有檔案**」。還原過程會暫停自動儲存規則，以確保下一次排定的 處理不會立即再次刪除已還原的檔案。當 本地副本處理完畢後，請重新啟用該規則。

還原功能會驗證密文、驗證解密過程、在 必要時進行解壓縮，並檢查原始明文 SHA-256，然後將檔案放置於 `media/`。 損壞的遠端物件絕不會取代本機檔案。若現有本機檔案的 位元組內容不同，系統會保留該檔案供審查，而非直接覆寫。

## 安裝資料遺失後的恢復方法

在另一台機器上安裝 TgWitness。使用私人還原檔案、另行 記錄的指紋，以及原始目的地的憑證：

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

對於 S3， `--credentials` 指向一個包含 `access_key` ，並 `secret_key`；經簽名的恢復檔案則提供目標設定。 此指令會使用直接外部連線，並在 rclone 遠端需要時下載已釘選的輔助程式 。若輸出目錄已存在，則會拒絕建立。

復原的原始位元組將寫入 `recovered-attachments/media/`，其名稱取自 其SHA-256。 `recovery-log.jsonl` 是一個未簽名的復原操作記錄。 此指令不會重建已遺失的簽名日誌或其簽名金鑰。請為這些資料保留 完整的工作區備份。儲存復原檔案並非完整的工作區 備份。

## 操作員機器人與完成通知

此 Telegram 機器人歸營運者所有。請透過 BotFather 建立該機器人，並在控制面板中設定其 代幣、目標聊天室以及明確允許的 Telegram 使用者 ID。發送者與聊天室 兩者必須完全吻合。轉發的訊息以及來自其他 機器人的指令將被忽略。

`/status` 且 `/stats` 在預設的「僅狀態」模式下皆可使用。可選的 控制模式則新增 `/pause`, `/resume` 和 `/copy`. `/copy` 並觸發已設定的 儲存任務；這並不表示遠端上傳已然完成。指令 無法傳入任意的 URL、檔案或 shell 程式。

請分別使用「警示」與「任務完成」的獨立通知設定。完成 通知會區分「存在缺漏的帳戶匯出」與「完整的匯出」，並顯示 歷史紀錄及儲存次數。除非在通知設定中另行 啟用，否則訊息摘錄不會包含在內。服務選擇器是根據實際 安裝的 Apprise 目錄所產生，而非一組固定的提供者範例。
