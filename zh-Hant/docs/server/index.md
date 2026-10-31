# 讓它持續運作

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/server/

確保資料收集器在系統重新啟動後仍可正常運作，且其資料保持完整。

## 選擇啟動方式

若要進行原生安裝，請使用 [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) 目錄中的[啟動](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/start/)程式及服務範例。若使用 Docker，請先安裝 Docker with Compose，並從專案目錄執行：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

預設控制面板會監聽主機的迴路位址，埠號為 8787。您可於本地端開啟，或透過 SSH 隧道連線。請使用第二條指令產生的憑證來解鎖控制面板。

## 請保留整個資料目錄

原生安裝使用 `data/live`。Docker 則使用持久化 `tgwitness-data` 卷。請將日誌、帳戶會話、金鑰及運作狀態集中存放。簽名導出檔雖是有效的證據，但並非完整的安裝備份。

1. 在執行完整備份之前，請停止資料收集。
2. 將完整的私有資料目錄複製到主機外的受保護儲存空間中。
3. 在依賴備份之前，請先於隔離環境中測試還原功能。

## 重新啟動後請確認

請確認預期的工作區與金鑰、Telegram 連線、已選定的來源以及新訊息擷取設定。儲存的 MTProto 狀態與補擷功能可協助恢復 Telegram 仍保留的更新內容。但無法重建所有已過期的更新，亦無法還原在擷取前已被刪除的編輯內容。

容器狀態良好意指網頁伺服器能正常回應。請使用受控訊息及見證檢查，以評估資料收集與外部發布狀況。

## 僅發布您有意發布的內容

部署參考指南包含 HTTPS 範例、持久化卷命令、更新及還原步驟。文中提供 Docker 命令以供部署；[目前的驗證記錄列出了](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/)實際經過測試的環境。
