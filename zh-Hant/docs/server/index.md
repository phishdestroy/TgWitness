# Telegram · 讓它持續運作

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/server/

讓收集器持續執行，資料在重新啟動後依然安全。

## 選擇啟動方式

原生：[啟動器](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/start/)加上 [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 中的服務範本。Docker，在專案資料夾中執行：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

面板監聽 localhost:8787。在本機或透過 SSH 通道開啟，使用第二個指令輸出的權杖。

## 請保留整個資料目錄

原生：`data/live`。Docker：`tgwitness-data` 磁碟區。日誌、工作階段和金鑰必須放在一起。簽名匯出是證據，不是備份。

1. 先停止收集。
2. 將整個資料目錄複製到主機以外的安全位置。
3. 在信任它之前，先在另一個安裝上試著還原。

## 重新啟動後請確認

檢查工作區和金鑰、連線、來源，以及新訊息是否進來。TgWitness 會補上 Telegram 仍保留的內容，而不是停機期間發生的一切。

容器「健康」表示網頁伺服器有回應。收集是否正常，要看測試訊息和見證人。

## 僅發布您有意發布的內容

HTTPS、磁碟區、更新和還原請見部署參考。實際測試過的內容：[驗證紀錄](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/)。
