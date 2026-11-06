# 已測試的內容

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/

Telegram 即時測試、自動化檢查、瀏覽器檢查，以及尚未經核實的內容。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | 結果 | 範圍 |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | 記錄 | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| 檢查 | 結果 | Qualification |
| --- | --- | --- |
| Core pytest | 1,461 passed | 37 platform skips |
| Browser / browser UX / evidence / site | 102 / 66 / 15 / 9 passed | These programs overlap other tests; counts are not additive |
| Capture addon | 124 passed | Three Official Web checks blocked by the required Chromium sandbox |
| API authorization | 269 routes; 538 requests passed | Missing credentials and revoked access |
| Retained archives | 48 of 48 verified | 3,598,381 records; pinned workspace keys |
| Live fleet read checks | 24 of 40 profiles passed | 16 WARP routes failed qualification; those profiles were not connected |

The [signed report](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) records all open findings, including three defects in an unpublished secret-chat snapshot absent from the audited main build. The earlier [public-history qualification](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) used a different revision and workload; its rates must not be combined with this comparison.

Verify the original report using the [pinned key and verifier](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Its signature protects the operator's report from alteration. It is not independent attestation, proof of Telegram authorship or GDPR certification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Phala Cloud 即時部署 · 2026 年 11 月 4 日

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| 設定 | Recorded value |
| --- | --- |
| 提供者 | Phala Cloud · `tdx.small` · US-WEST-1 |
| 部署 | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

前兩次部署發現與模擬的 Phala Cloud 有五處差異。 [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) 現已能重現每項差異，若未進行修正則會失敗：

| 在 Phala Cloud 上 | 修正前 | 修正 |
| --- | --- | --- |
| 必須指定 `compose_file.name` | HTTP 422 錯誤，未建立任何內容 | Docker Compose 配置中包含 CVM 名稱 |
| 除非指定為空，否則 Phala 會將其自身的啟動前腳本新增至被測的 app-compose 中（v0.0.20：Docker 登入、`docker compose pull`、root 密碼、來自 `user_config` 的 SSH 金鑰） | `tdx_compose` 失敗：程式碼超出已發佈的 Docker Compose 配置範圍 | app-compose 將 `pre_launch_script` 設定為 `""`；Phala 隨後會將其省略 |
| 若未指定 `image`，Phala 會預設選用 `dstack-dev-0.5.12`（開發版），且此版本已啟用 SSH 存取權限 | `server_state` 失敗。此映像僅有硬體驗證記錄通過；僅供應商記錄與 `tdx_os` 顯示此結果 | 部署過程會要求使用 Phala 當前版本（`dstack-0.5.12`）的生產環境建置版本 |
| 當 dstack 閘道器關閉時，CVM 詳細資訊中永遠不會出現 `instance_id` | 部署等待 30 分鐘後失敗 | 實例 ID 取自 CVM 狀態 |
| 重新啟動、停止及啟動均屬 CVM 操作，而非應用程式版本更新 | `provider_actions` 未列出重新啟動紀錄 | 這些操作也包含讀取操作 |

**Deployment 3 · attestation, access checks and restart evidence**

- 該 CVM 在關閉 SSH 存取的情況下執行 `dstack-0.5.12`。收集器在建立後約 1.5 分鐘發布其簽名位址。部署後通過 `tdx_binding`、`tdx_quote`（Intel TCB UpToDate、硬體驗證記錄 v4、FMSPC `20a06f000000`、非除錯模式、不可遷移、支援從 Intel 擷取的 加密驗證資料）、`tdx_compose_hash`、`tdx_compose`（逐位元組）以及 `tdx_identity`（KMS 金鑰）。
- 位於 trycloudflare.com 網址的控制面板在未提供令牌或提供錯誤令牌時會返回 401 狀態碼， 而使用控制面板令牌時則會返回 200 狀態碼。
- `verify` 搭配 `--source` 設定為 GitHub 的提交存檔，且指紋已 另行通過：伺服器、`server_state`、防火牆（無閘道、無公開端點）、供應商日誌、 帳單明細、指紋、來源雜湊、開機，以及五項 `tdx_*` 檢查均通過。 Cloudflare 及 `tdx_os` 無法取得，因此結果為「不完整」。
- 透過 Phala 的 API 執行兩次重新啟動：每次 CVM 都在兩分鐘內恢復運作，並使用 相同的收集器金鑰、新的簽名位址，而舊的位址則回傳 530 狀態碼。`verify` 將 新的開機及兩次重新啟動皆報告為 REVIEW。 透過 `--evidence`，系統確認了日誌 簽名以及三次啟動，每次皆擁有來自同一 CVM 的獨立 Intel TDX 硬體驗證記錄。
- `destroy` 僅移除了該 CVM。隨後工作區變為空狀態，且控制台網址停止 回應。
- 控制台精靈的價格查詢顯示 `tdx.small`，每小時 0.058 美元。若輸入錯誤的金鑰，則會顯示 「未接受該 API 金鑰」的純文字訊息。

**Follow-up fixes · signed address discovery and OS measurements**

- 若無地址金鑰，`verify` 會遵循關於地址主題的最新且格式正確的貼文， 該貼文印在已發佈的 Docker Compose 配置中。一則偽造的貼文將其傳送至一個不 存在的宿主，導致 `statement` 失敗：偽造者無法冒充收集器，但能阻擋 第三方驗證，透過偽造的未來時間戳記，最長可阻擋長達 12 小時。收集器現在 也會發佈以其自身金鑰簽署的地址，當 收集器發佈此類貼文時，`verify` 僅接受此類貼文，且貼文會依照 ntfy.sh 的接收時間排序。 [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) 會重播這些偽造的發布。CVM 僅會從包含此程式碼的提交中執行此程式，因此本次執行的收集器尚未簽署其地址， 而 `verify` 亦已指出此情況。
- `tdx_os` 原先依賴 `dstack-mr`，而該工具目前的版本提供的是 `measure-os`，並非文件中提到的 `measure --json`。驗證器現在會根據已發布的映像檔和虛擬機器設定（包含 ACPI 表格）自行計算 MRTD 和 RTMR0-2。

**Deployment 4 · all 16 checks, report seals and restart verification**

- 部署程序曾一次下載已發佈的 `dstack-0.5.12`，並將其與 CVM 回報的作業系統映像雜湊值進行比對，而 `tdx_os` 通過驗證：MRTD、RTMR0、RTMR1 及 RTMR2 均等於針對 QEMU 8.2.2、1 個 vCPU 及 2 GiB 所計算的數值相符。然而，針對聲稱具備 4 GiB、2 個 vCPU、 QEMU 9.2.1 或第二張網路卡的配置，相同計算方式得出的 RTMR0 數值則不同；若內核、韌體或命令列 發生變更，以及針對開發版映像，驗證均會失敗。
- `verify` 通過了全部 16 項檢查（包含快速隧道連接器），因此結果 為「通過」。 它寫入了 HTML 和 PDF 憑證，並以數位印章加蓋簽名與時間戳記，其中包含來自 比利時政府時間戳記單位 TSU 202301（已列入比利時可信 清單）的合格 eIDAS 時間戳記、FreeTSA 時間戳記以及驗證者的簽名；`check-report` 確認了所有這些 內容以及 PDF 文件的簽名。
- 重新啟動後，`verify --evidence` 確認了兩次啟動，每次均伴隨在 CVM 內部生成的硬體驗證，且每次 皆從已發佈的 `dstack-0.5.12` 啟動；重新啟動與新一次的啟動均為 REVIEW 狀態。
- `destroy` 使工作區保持空置狀態。

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- 該收集器在其地址旁發布了以自身金鑰簽署的地址，緊鄰操作員的 HMAC 貼文。 隨後，該主題中新增了兩則偽造貼文，一則 HMAC 值為零，另一則由另一把 Ed25519 金鑰簽署，兩者均聲稱時間為 2096 年。 `verify` 採用由 收集器金鑰簽署的地址，並通過了全部 16 項驗證；該印章再次附有符合資格的比利時時間戳記、 FreeTSA 的時間戳記以及驗證者的簽名，而 `check-report` 則確認了這些資訊。
- 重新啟動後，收集器發佈了經簽名的全新位址：`verify` 立即偵測到該位址， 營運商的 **透過 HMAC 發佈，於 27 秒後偵測到當前位址**，兩者均忽略了 偽造的發佈。`verify --evidence` 確認有兩台裝置從 `dstack-0.5.12` 啟動。
- 部署過程列出了 Phala 向 CVM 收取的費用（含磁碟空間）：每小時 0.06078 美元。

### Panel wizard and remaining scope

面板精靈在 Phala Cloud 上執行了兩次，一次透過其工作 API，另一次則透過 搭載真實 Chromium 核心的瀏覽器：價格查核、以 **Advanced** 為提交標籤進行建立，全部六項 驗證檢查均通過，伺服器清單顯示計費價格（每月 44.37 美元）， **Find 當前位址**、下載已量測的 Docker Compose 配置，以及刪除操作。瀏覽器未出現任何頁面錯誤。 每次操作結束後，工作區均呈空狀態。

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

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

## 對一百萬則訊息進行全文搜尋 · 2026年11月5日

指令： `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

包含 200 個聊天室中 1,000,000 則合成訊息（俄語 詞形、烏克蘭語、英語、中文、日語、連結及識別碼）的確定性簽名日誌，於 71 秒內完成索引；該索引佔用 58 MiB 空間，此外還有 1.50 GiB 的日誌檔案。 最佳匹配 搜尋耗時 9 至 190 毫秒（中位數），相較之下，先前子字串 搜尋則需 2.4 至 3.2 秒。完整結果、硬體配置與限制：[全文搜尋](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/search/#benchmark)。 `tools/test_fulltext.py` 亦會使用當前驗證器驗證在全文搜尋 （`tools/fixtures/evidence-before-fulltext.zip`）使用當前驗證器進行驗證，並使用該歸檔檔自身的 驗證器對當前 歸檔檔進行驗證。 `verify.py`.

## 其餘資格說明

所保留的即時日誌可記錄實際的訊息收集、編輯、刪除通知、附件、 重新檢查及速率限制處理。 它並未完整記錄訊息送達狀況，亦未建立受控的 角色可見性矩陣、反應主體、延長的 FloodWait、帳號封禁以及 網路／程序中斷恢復等資訊。QR 代幣的發行仍與已完成的 行動端 QR 碼確認程序有所區別。

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
