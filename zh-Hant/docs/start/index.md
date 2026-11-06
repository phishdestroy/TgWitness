# Telegram · 幾分鐘內即可開始使用

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/start/

先在展示版中隨意看看，再連接您自己的帳戶。

## 無需註冊即可瀏覽

取得專案，準備好 **Python 3.11 或更新版本**，執行展示版。其餘的由啟動器處理。

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

瀏覽器會開啟一個含虛構訊息的工作區。開啟聊天室，比較一次編輯，看看一份匯出。不涉及 Telegram。

![TgWitness 對話檢視畫面及範例訊息](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

一個範例工作區。您的個人日誌將另行建立。

## 建立您自己的工作區

關閉展示版，然後：

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

開啟啟動器顯示的網址，貼上它所指檔案中的**面板存取權杖**。這是 TgWitness 的權杖，不是 Telegram 的。

## 擷取您的第一則訊息

1. [連結一個專用的 Telegram 帳號。](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/accounts/)
2. 選擇一個群組或頻道，開始觀察。
3. 在測試群組中傳送一則訊息，看著它出現在日誌中。

若要進行伺服器安裝，請參閱「[保持運作」指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/server/)。
