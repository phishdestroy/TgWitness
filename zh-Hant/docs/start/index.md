# 幾分鐘內即可開始使用

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/start/

首先，請參閱一個實際運作範例。接著，請連結您的帳戶。

## 無需註冊即可瀏覽

下載或克隆該專案，安裝 **Python 3.11 或更新版本**，並執行示範程式。啟動程式會建立本地環境並安裝已標記的依賴項。

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

瀏覽器將開啟一個包含虛構訊息的工作區。您可開啟對話、比對編輯內容，並檢視匯出檔案。示範模式不會連線至 Telegram。

![TgWitness 對話檢視畫面及範例訊息](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

一個範例工作區。您的個人日誌將另行建立。

## 建立您自己的工作區

結束示範流程後，請使用標準啟動程式：

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

開啟啟動器顯示的本地位址。若系統提示，請輸入終端機中指定之本地檔案內的**面板存取憑證**。此操作將解鎖 TgWitness；此程序與 Telegram 的登入程序是分開的。

## 擷取您的第一則訊息

1. [連結一個專用的 Telegram 帳號。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/accounts/)
2. 請選擇該帳號可存取的群組或頻道，然後開始監測。
3. 在您所控制的測試群組中發送一則新訊息，並確認該訊息是否出現在日誌中。

若要進行伺服器安裝，請參閱「[保持運作」指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/server/)。
