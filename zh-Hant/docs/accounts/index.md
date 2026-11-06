# Telegram · 連結帳戶

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/accounts/

一個工作區 = 一個帳戶、它的日誌和它的金鑰。

## 選擇登入方式

**帳戶** → 新增工作區 → 連線設定。請為此使用另一個帳戶。

- **QR 碼：**在 Telegram 的「裝置」畫面掃描並確認。
- **電話號碼：**號碼、驗證碼，若有兩步驟驗證再輸入密碼。
- **匯入工作階段：**您自己的工作階段檔案或 Telegram Desktop 資料。

使用內建 API 設定檔或您自己的 API ID 和 hash。它只用來識別應用程式，不會讓您登入，也不會隱藏任何東西。

**需要先設定代理伺服器嗎？**

您可以在登入前[選擇並測試連線路徑](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/proxies/)。每個帳戶皆有其專屬的路徑。

## 選擇監測對象

1. 選擇您需要的聊天室、群組或頻道。
2. 檢查收集設定，包括媒體。
3. 啟動後檢查連線和最近活動。

帳戶必須有存取權。管理員和成員看到的內容不同，日誌顯示的是這個帳戶收到的內容。

整個帳戶？**來源 → 觀察範圍 → 調查模式**，檢查後按**儲存範圍**。完整步驟：[調查整個帳戶](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/cases/)。

## 檢查完整路徑

在測試群組中，用另一個帳戶傳送一則訊息，編輯它，再刪除它。這三個事件都應出現在日誌中。然後[匯出並驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/exports/)。

「已連線」表示連線正常。捕捉到測試訊息才代表事件確實送達。

## 新增另一個帳戶

在**帳戶**中新增工作區，步驟相同。請記下每個帳戶的金鑰指紋，以便日後區分匯出。
