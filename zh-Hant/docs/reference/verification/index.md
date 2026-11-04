# 已測試的內容

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/

Telegram 即時測試、自動化檢查、瀏覽器檢查，以及尚未經核實的內容。

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | 計數 |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| 檢查 | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Telegram 即時測試，完整帳戶 · 2026年10月29日

在進行以下測試後，該帳號仍持續運作。10月29日 UTC 12:10，其監控範圍 已切換至整個帳號（頻道、群組、私人聊天室及機器人）；控制面板要求 確認，並由簽名日誌記錄此操作。截至 UTC 17:59，日誌內容如下：

| 記錄時間：10月27日 21:36 至 10月29日 17:59（UTC） | 計數 |
| --- | --- |
| 日誌記錄 | 9,968 |
| 新訊息 | 5,308 |
| 在切換至完整帳戶後，其中一部分 | 3,878 |
| 刪除記錄 | 784 |
| 其中部分訊息在 TgWitness 儲存該訊息後被刪除 | 596 |
| 編輯 | 41 |
| 經重新核對後新增的訊息 | 2,273 |
| 經重新檢查後已無法找到的訊息 | 18 |
| 透過歷史快照儲存的訊息 | 242 |
| 已儲存的附件 | 247 |
| 收集器啟動 | 19 |
| Telegram FloodWait 暫停 | 26 |

- 該小組的「**Verify」**核查已確認所有 9,968 筆記錄的簽名與雜湊鏈。
- 訊息來自 2 個群組或頻道，以及 3 個私人聊天室和機器人。其中有一次是在「**聊天室**」中 按下訊息按鈕；該請求及 Telegram 的回應均記錄於日誌中。
- 當收集器在重新啟動時重新掃描該帳戶時，新增了聊天室。由於 「儲存新聊天室的早期訊息」功能已關閉（`history = 0`），因此此處不予說明。

未涵蓋內容：反應、成員變動、個人檔案、發送訊息、透過 邀請加入、代理伺服器、通知、witness 機器人以及同時管理多個帳戶。公開檔案 僅包含計數資料。

## 透過 libarchive 開啟受密碼保護的匯出檔案 · 2026年10月29日

由匯出加密程式碼所建立的壓縮檔（WinZip AES-256 格式，7-Zip 和 WinRAR 可讀取），已透過 Windows 版 `tar`（bsdtar 3.6.2、libarchive）開啟。 輸入正確密碼後， 解壓縮後的檔案與原始檔案的 SHA-256 值相符；輸入錯誤密碼則會顯示「密碼短語不正確 」而遭拒絕。7-Zip 和 WinRAR 本身並未被執行。

## Telegram 即時測試 · 2026年10月27日至29日

一個真實的 Telegram 帳戶，透過內建的 API 配對池登入，記錄了某個 超級群組自 **10 月 27 日 21:36 UTC 至 10 月 29 日 05:15 UTC** 期間的訊息。在此期間， 資料收集器共啟動了 12 次。

| 已記錄 | 計數 |
| --- | --- |
| 日誌記錄，包含心跳訊號與服務記錄 | 2,385 |
| 新訊息 | 1,291 |
| 刪除記錄 | 472 |
| 其中部分訊息在 TgWitness 儲存文字後被刪除 | 347 |
| 編輯 | 12 |
| 暫停期間遺漏的訊息，已透過重新檢查補入 | 12 |
| 已儲存的附件 | 17 |
| 未下載附件（下載功能已關閉，或無檔案可下載） | 14 |
| Telegram FloodWait 在重新檢查時會暫停，每次暫停 3 秒 | 8 |

- 所有 2,385 筆記錄的簽名與雜湊鏈，皆可透過該日誌的 公鑰進行驗證。
- 重新啟動後，收集器將從儲存的更新狀態（`pts`）繼續運作，而 Telethon 會進行補齊；隨後的重新檢查則會新增仍缺失的訊息。
- 在每次 FloodWait 事件中，資料擷取器會等待指定時間後再繼續執行。
- 該帳號保持登入狀態，且同一會話於 10 月 29 日重新連線。

本次測試未涵蓋的項目：同時處理多個帳戶、管理員角色、代理伺服器、 持續數小時以上的服務中斷，以及完整的[即時驗收程序](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)。 公開檔案僅包含上述統計數據：不包含任何帳戶或聊天室識別碼、訊息或 憑證資訊。

## 合成本地能力測量

指令：`python tools/check_capacity.py --events 10000 --chats 100`

| 指標 | 觀察到 |
| --- | --- |
| 輸入 | 涵蓋 100 個精選合成來源的 10,000 則合成訊息事件 |
| 訊息內容 | 400 個字元；不含媒體或網路內容 |
| 資料擷取 | 53.273 秒；每秒 187.7 次事件 |
| 處理器延遲 | p50 4.162 毫秒；p95 7.784 毫秒；最大值 129.118 毫秒 |
| ZIP 匯出 | 啟用 tracemalloc 時耗時 19.868 秒 |
| Python 匯出區塊的峰值追蹤 | 0.51 MiB；不處理 RSS |
| ZIP 檔案大小 | 4,610,962 位元組 |
| 獨立驗證 | 所有 10,000 筆事件均已驗證 |

此測量針對本 Windows 主機上的本地序列記錄／匯出路徑。它 不測量 MTProto 傳輸、並行帳戶、Telegram 流量限制、媒體檔案、 長期運行的負載，亦不保證實際聊天數目。此測量是在 最終離線時間戳工具推出之前進行的，該工具並不會改變所測量的訊息路徑。

## 其餘資格說明

所保留的即時日誌可記錄實際的訊息收集、編輯、刪除通知、附件、 重新檢查及速率限制處理。 它並未完整記錄訊息送達狀況，亦未建立受控的 角色可見性矩陣、反應主體、延長的 FloodWait、帳號封禁以及 網路／程序中斷恢復等資訊。QR 代幣的發行仍與已完成的 行動端 QR 碼確認程序有所區別。

Docker 建置／執行、Linux／macOS 安裝、持續高負載、獨立安全 審查、真正的獨立 TSA 回應、憑證撤銷／歸檔驗證以及 鑑識認證仍不在本次記錄的認證範圍內。已實作 MTProto 狀態 儲存與補錄功能；原子性持久重播功能尚未建立。 管理日誌 收集、額外的反應器清單以及優先級短輪詢仍屬獨立功能。 請參閱[即時驗收](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)報告以了解受控資格認證矩陣。

本地詳細收據與螢幕截圖位於 test-results/ 目錄下（Git 已忽略）。 docs/assets/ 目錄中的公開螢幕截圖僅包含虛構的示範資料。
