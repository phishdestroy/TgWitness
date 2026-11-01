# 本地 OCR 與文字轉錄

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/media-analysis/

透過本地工作程序識別擷取的圖像與音訊；並將衍生的文字與其原始檔案保持關聯。

[工作流程指南](https://phishdestroy.github.io/TgWitness/docs/archive/) · [維基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

開啟一份 `media.saved` 日誌記錄，選擇「**識別附件**」，然後在「**查詢存檔」**下選取 OCR 或轉錄。處理過程為手動且在本地進行。 本工具不提供雲端媒體模式或自動上傳功能。原始附件位元組與 `media_sha256` 均保持不變；辨識出的文字會明確標示為機器 辨識結果，並與來源雜湊值、引擎／模型版本、 語言、參數及完成時間分開儲存。轉錄內容會保留原始的時間戳記。

請使用**「搜尋已識別文字」**功能及 OCR/文字轉錄 篩選器來搜尋這些結果。這是一項獨立的衍生資料搜尋；它不會在未經通知的情況下將機器 識別結果轉換為原始 Telegram 文字，也不會將其新增至已簽署的事件中。

## 設定可選的工作程序

第 1 版需要配備本地 Docker 守護程式的 Linux 主機。Windows 系統 可於具備獨立本地守護程式的 Linux 虛擬機器／WSL 環境中運行 TgWitness。 該面板絕不會自行解碼任何未經信任的附件。

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

請在 TgWitness 服務環境中設定這些變數，並重新啟動服務。 守護程序套接字預設為 `/var/run/docker.sock`；無 root 權限的部署可設定為 `TGWITNESS_DOCKER_SOCKET`。工作程序會明確使用該 Unix 套接字， 而非遠端 Docker 環境。請勿向控制面板使用者公開 Docker API，亦請勿將 其套接字掛載至識別容器內。

若需進行文字轉錄，請另行安裝與 CTranslate2 相容的 Whisper 模型， 然後將 `TGWITNESS_WHISPER_MODEL_DIR` 設定為該模型的目錄。工作節點會透過 `local_files_only=True` 載入該模型；所選模型與輸入資料將以唯讀方式掛載。 請參閱引擎的[模型載入文件](https://github.com/SYSTRAN/faster-whisper)。 隨附的 OCR 映像檔包含英文和俄文的訓練資料。如有需要，可將其他 語言整合至您的映像檔中；語言代碼遵循 [Tesseract 的命令列介面規範](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html)。

處理過程中不會載入任何模型。建置／下載設定程序可能會使用網路； 每個實際的辨識容器均已停用網路連線。請在啟用網路前安裝映像檔； 執行時使用 `--pull=never`。

## 限制與資料復原

該容器以無特權使用者身分運行，具備唯讀 root 權限、已降級 的權能、`no-new-privileges` 模式、1 個 CPU、2 GiB 記憶體、PID 限制以及受限的 臨時檔案系統。僅掛載所選檔案的驗證副本及可選的 模型目錄。 收集器的資料庫、儲存庫及工作階段 均未掛載。[Docker 執行時參數會](https://docs.docker.com/reference/cli/docker/container/run/) 強制執行這些限制；此仍屬容器邊界，而非硬體隔區。

檔案大小上限為 50 MiB，圖片上限為 2,000 萬像素，音訊上限為 30 分鐘（ 且須為已知時長），處理時間上限為 5 分鐘。每次僅能執行一個工作程序， 每個工作區最多可排隊或執行 20 個工作，並保留 100 個工作。 「取消」會停止容器；「重試」會建立一個與先前嘗試相關聯的新工作。 中斷的工作在重新啟動後會被標記。當模型 無法符合設定的限制時，處理可能會失敗；若未進行隔離，系統不會在無提示的情況下繼續執行。
