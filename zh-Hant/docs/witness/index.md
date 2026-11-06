# 設定 Witness 機器人

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/witness/

一個獨立程序檢查您的日誌，並將簽名檢查點發布到頻道。

## 兩台主機，兩組簽名金鑰

部署 / 資料收集器**帳戶 + 日誌**

Telegram 會話收集器的簽名金鑰

唯讀檢查點端點

← 請求簽署的回答 →

主機 B / WITNESS**驗證 + 保留**

固定收集器指紋 獨立的見證簽署金鑰

專屬日誌 + 機器人代幣

Witness → Telegram 機器人 API →**您的頻道 · 經簽名的 TGW1 貼文**

Witness 會自行執行驗證。收集器的存取權限為唯讀。機器人發佈時會使用 Witness 的連線與憑證；Witness 不會獲得任何帳戶會話權限。

03 / 檢查點決策示例答案

最後接受日期**120 筆記錄**`head 9c7d…`

下一則答案**128 筆記錄**`head a4f2…`

已接受：計數持續增加，簽名經驗證無誤，且金鑰匹配。該見證者保留此新界限。

所有解答範例均假設具備有效簽名及已釘選的金鑰。此處的雜湊值僅為簡化示意。單憑較大的計數並不能證明整個舊前綴未曾變更；請將匯出資料與保留的檢查點進行比對。

## 準備一個機器人與一個頻道

用 BotFather 建立機器人，並允許它在您的頻道中發文。請在別處執行見證人：另一台主機，最好由其他人管理，遠比在收集器旁多跑一個程序更有價值。

## 「進階功能」中的三個步驟

1. **唯讀存取。****擴充功能 → 獨立見證人**，建立權杖並儲存檔案。它只讀取檢查點和健康狀態，別無其他。
2. **頻道和間隔。**Telegram 頻道或 Discord webhook，以及見證人能連到的收集器網址。儲存設定檔。
3. **啟動。**將 `witness.json`、`witness-token.txt` 和 `bot-token.txt` 一起放到見證人主機上並執行：

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

等待頻道中出現第一則簽名貼文，然後將見證人指紋保存在安全的地方。

想用 Discord？將 webhook URL 儲存為 `discord-webhook.txt`。一個見證人只發布到一個地方；較長的檢查結果在 Discord 上以檔案形式送達。

## 選擇發布頻率

每次檢查都發文可以形成穩定的外部紀錄：每五分鐘一次，約等於每個工作區每天 288 則貼文。進階設定可以只在有變化或出問題時發文，使用代理或自訂 Bot API。

**該機器人實際上能證明什麼？**

它向收集器請求簽名檢查點，以預期的金鑰核對，並保存自己的簽名日誌，包括錯過和被拒絕的回應。

它檢查的是日誌狀態，本身並不監看 Telegram。為此，請執行受控的送達測試。

## 稍後查閱證據

請保留見證人日誌、貼文和指紋。[如何核對它們](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/#verify)與收集器匯出是否一致。
