# 高可信度部署

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/

位於 Hetzner 或 Phala Cloud 上的全天候密封伺服器、Gateway DNS，以及第三方可重複驗證的檢查機制。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [文件說明](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [部署與復原](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/deployment/)

![部署與復原](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

高可信度部署會在 檔案驗證過程中，額外加入對資料蒐集環境的獨立檢查。審查人員會查詢由 雲端服務供應商及 Cloudflare 持有的部署與存取紀錄，而 Intel TDX 部署則會針對 資料蒐集器的環境進行硬體驗證。

一般的本地端及 Docker 使用方式維持不變。除非您使用 `python -m tgwitness.cloud`進行部署，且收集器僅在部署設定為 `TGWITNESS_ASSURANCE`.

流程圖 · 操作員 → 伺服器、未設定進站規則的防火牆 (提供者 API); 操作員 → 隧道與 DNS (Cloudflare API); 伺服器、未設定進站規則的防火牆 → 隧道與 DNS (僅限外發); 伺服器、未設定進站規則的防火牆 → 在伺服器上建立的簽名金鑰; Verifier，唯讀代幣 → 提供者日誌與防火牆; Verifier，唯讀代幣 → 隧道連接器地址與入口; Verifier，唯讀代幣 → 已簽署的 /api/assurance 聲明; Verifier，唯讀代幣 → 證據 ZIP 檔案 · 操作員 · Verifier，唯讀代幣 · 伺服器、未設定進站規則的防火牆 · 提供者日誌與防火牆 · 隧道連接器地址與入口 · 已簽署的 /api/assurance聲明 · 證據 ZIP 檔案 · 隧道與 DNS · 在伺服器上建立的簽名金鑰 · 提供者 API · Cloudflare API · 僅限外發

**圖表轉為文字**

1. 操作員 → 伺服器、未設定進站規則的防火牆 (提供者 API)
2. 操作員 → 隧道與 DNS (Cloudflare API)
3. 伺服器、未設定進站規則的防火牆 → 隧道與 DNS (僅限外發)
4. 伺服器、未設定進站規則的防火牆 → 在伺服器上建立的簽名金鑰
5. Verifier，唯讀代幣 → 提供者日誌與防火牆
6. Verifier，唯讀代幣 → 隧道連接器地址與入口
7. Verifier，唯讀代幣 → 已簽署的 /api/assurance 聲明
8. Verifier，唯讀代幣 → 證據 ZIP 檔案

**本頁內容**

- [驗證者可檢查的內容](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#what-a-verifier-can-check)
- [提供者](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#providers)
- [Phala Cloud 上的機密虛擬機器 (Intel TDX)](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [開始之前](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#before-you-start)
- [來自控制面板](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#from-the-panel)
- [無需網域的快速隧道](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [部署](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#deploy)
- [除錯部署與鎖定](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#debug-deployment-and-lock)
- [移除部署](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#remove-a-deployment)
- [任何伺服器（自我認證）](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#any-server-self-attested)
- [驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#verify)
- [證據移交報告](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#report-for-evidence-handover)
- [Cloudflare 作為外部見證者](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [閱讀部署結果](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#reading-the-deployment-result)

## 驗證者可檢查的內容

| 聲明 | 如何進行驗證 | 維護者： |
| --- | --- | --- |
| 該伺服器是透過服務供應商的 API，於已知時間點建立的 | 伺服器物件及其在提供者自有日誌中的建立過程 | 提供者 |
| 沒有人使用該服務提供者的存取路徑 | 控制台請求、救援、密碼重設、重建、ISO、影像檔及備份的日誌 | 提供者 |
| 無法連線至該服務 | 服務提供商的防火牆沒有任何進站規則；SSH 連線自首次開機起即被隱藏 | 提供者（防火牆）、主機（SSH） |
| 該面板僅能透過隧道存取 | 隧道入口僅將流量轉發至控制面板；連接器則從伺服器位址運行 | Cloudflare |
| 此軟體的實際運作方式如下： | 收集器的簽名原始碼樹雜湊值等同於已部署提交的檢出內容 | Collector，已與 Git 比對 |
| 該簽署金鑰是在該伺服器上建立的 | 該金鑰會簽署一份聲明，其中載明服務提供者的伺服器 ID 以及其收到的 cloud-init 檔的雜湊值 | Collector，已與服務提供商進行比對 |
| 該日誌屬於該金鑰與伺服器 | 每個在證據 ZIP 中啟動的程序，皆包含該伺服器的主機測量值 | 證據 ZIP |

收集器會將 SSH 狀態、連線、登入歷史紀錄及開機資訊記錄於經簽名的 process-start 及 `host.state` 記錄中。在一般虛擬機器上，這些屬於本機清單 記錄，審查人員會將其與服務供應商的獨立記錄進行比對。下文所述的 Intel TDX 部署方案，則會額外驗證由硬體支援的測量結果。

## 提供者

| `--provider` | 憑證 | 驗證者的唯讀存取權限 | 驗證者專用的提供者日誌 | 保留用途： |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | 同一專案的讀取權限 | 伺服器與防火牆操作 | 只要這些資源存在 |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | 唯讀個人存取憑證 | Droplet 動作 | 只要 Droplet 存在 |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` 唯讀範圍 | 帳戶事件、防火牆規則版本 | 90 天 |
| `vultr` | `VULTR_API_KEY` | 具備讀取權限且擁有 `activity_logs` 權限 | 帳戶活動日誌（方法、路徑、執行者） | 30 天，若訂閱稽核日誌則可延長保存期限 |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrail 事件歷史紀錄 | 90 天 |
| `phala` | `PHALA_CLOUD_API_KEY` | 同一工作區的 API 金鑰 | 應用程式修訂與 CVM 操作：Docker Compose 配置與環境變更、重新啟動、作業系統升級 | 雖然該應用程式確實存在 |
| `generic` | 無 | 無 | 無：**自我驗證** | – |

請為每個案例使用專屬的專案、團隊、帳戶或子帳戶：驗證者的 唯讀存取權限將僅顯示此部署。憑證會從 `--provider-token-file` 或上述變數中讀取，絕不從命令列取得。對於 AWS，該檔案 儲存 `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`；區域為 `--location`.

每份報告中皆會列出各服務供應商的記錄所無法呈現的內容。 簡而言之：Hetzner 會記錄主控台請求；DigitalOcean 的 Recovery Console、Linode 的 Lish/Glish 以及 Vultr 的網頁 主控台並未以該形式被記錄，因此 root 帳戶在首次開機時即被鎖定，若要登入主控台 則需重設密碼或變更開機方式，而這些操作都會被記錄下來。Vultr 會將主控台 網址回傳給任何能讀取該實例的金鑰；無論是記錄還是報告中均不會儲存此資訊。

## Phala Cloud 上的機密虛擬機器（Intel TDX）

透過 `--provider phala` 收集器運行於 [Phala Cloud](https://phala.com/) 上的 Intel TDX 機密虛擬機器中， 並由 dstack 管理。主機與 Phala 工作人員均無法讀取其 記憶體，且處理器會針對該機器啟動的狀態簽署一份證明。驗證器不會 僅憑 Phala 的聲明就予以採信： `tgwitness.tdx` 會自行檢查每份證明——直至固定於 Intel SGX 根憑證授權機構（Root CA）層級——並對照 Intel 的撤銷清單及 Intel 簽署的平台資料，同時拒絕 任何可被除錯或遷移的機器。

| 報告條目 | 功能展示 |
| --- | --- |
| `tdx_binding` | 此證明涵蓋收集者的簽名聲明以及本次請求的隨機值 |
| `tdx_quote` | Intel 為此認證背書；唯有當 Intel 評定該平台為最新版本時，才算通過認證 |
| `tdx_compose_hash` | RTMR3 從 dstack 事件日誌中重播資料，並測量收集器所回報的應用程式編寫情況 |
| `tdx_compose` | 該編譯結果與已部署提交的程式碼完全字節對字節一致：原始碼檔案透過雜湊值固定，兩張圖片則透過摘要值固定，沒有其他程式碼 |
| `tdx_identity` | 此證明來自已部署的應用程式與實例，並使用 Phala 的 KMS 所提供的金鑰以及加密磁碟 |
| `tdx_os` | MRTD 和 RTMR0-2 的數值等同於驗證器根據 Dstack-TEE 發布的 dstack 作業系統映像所計算的數值，該數值是透過 CVM 回報的作業系統映像雜湊值，以及 QEMU 根據虛擬機型態所建立的 ACPI 表格（包含韌體、核心、initrd、附帶根檔案系統雜湊值的命令列、記憶體、vCPU 及裝置）所推算得出。開發用映像會導致驗證失敗 |

作業系統映像檔（約 180 MB，其中保留 21 MB）會從 [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) 下載一次至 記錄旁的 `dstack-images`；`--tdx-image FOLDER` 使用另一個資料夾或已解壓縮的映像檔， `--tdx-image none` 則跳過比對步驟。 測量步驟依循 `dstack-mr` 及來自 Dstack-TEE/dstack 的 `qemu-acpi` Rust 套件；`tools/check_dstack_image.py` 會將其與 QEMU 自身的 ACPI 輸出以及真實的 Phala Cloud 硬體認證記錄進行比對，`--live` 則會與已發布的映像進行比對。 `--tdx-measurements` 則仍會比較以 JSON 格式提供的 MRTD 與 RTMR0-2。

日誌中記錄的每次收集器啟動都附有此類證明，因此 `verify --evidence` 會檢查每次啟動及其所啟動的作業系統映像。Phala 的應用程式修訂版本 以及 CVM 的運作狀況即作為供應商日誌：若 Docker Compose 配置在部署後發生變更， 報告將被判定為失敗，且重啟紀錄會被列出以供審查。

在面板中，選擇**「額外功能** 」→「**24/7 伺服器** 」下的**「機密虛擬機器 · Phala Cloud」** ，並貼上 Phala Cloud API 金鑰；快速隧道運作方式與 Hetzner 相同。若透過命令列操作：

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` 從檔案中讀取 Intel 的憑證和撤銷清單，而非 從 Intel 下載。此處無法使用 Gateway DNS：Phala 沒有針對 外發流量的服務供應商防火牆。

### 驗證憑證

對於 Phala 部署，`verify --report certificate.md` 還會寫入憑證：一個 獨立的 `certificate.html` 及一份 A4 規格的 `certificate.pdf`，內容包含驗證結果、從 Intel 根憑證到收集器金鑰的信任鏈、 與普通及高保障級別伺服器的比較、 實際測量值與根據已發布映像計算出的數值的對照、各部分的擔保方、 Intel 憑證鏈、每項檢查、供應商日誌，以及如何重現 驗證流程。 JSON 報告仍是權威性紀錄；這些頁面僅是其呈現形式。

本報告已透過簽名與時間戳記進行數位加封，相關內容存於 `certificate.seal.json` 以及其旁之 `.tsq`/`.tsr` 檔案中：

| Seal | 新增功能 |
| --- | --- |
| 合格電子時間戳記，`http://tsa.belgium.be/connect` | RFC 3161 時間戳記，基於比利時聯邦政府合格信任服務提供者（FPS 政策與支援局，BOSA）所提供的 `certificate.json` 精確位元組資料。 該單位被列為比利時歐盟可信清單中的「合格時間戳記服務」，狀態為「已授予」；截至 2026 年 10 月 20 日發布的清單，其根憑證（比利時根 CA6）及清單中的條目均已固定於 `tgwitness/tsa_roots.py` 中。 根據《歐盟法規》第 910/2014 號第 41 條，此類時間戳記在每個歐盟成員國內，其日期、時間及資料完整性均被推定為準確無誤。 |
| RFC 3161 時間戳記，FreeTSA | 第二個獨立的時間戳記 |
| 驗證器簽名 | Ed25519 基於一項聲明，該聲明列出報告的 SHA-256 值及所有時間戳記，並使用驗證者自身的金鑰（`--sign-with FOLDER`，預設為 `~/.tgwitness/verifier`）；該 PDF 文件附有由同一金鑰簽署的數位簽章 |

`--timestamp URL`（可重複）選擇其他授權機構，`--timestamp none` 不選擇任何機構，`--sign-with
none` 則不對印章進行簽署。`check-report` 會檢查報告的雜湊值、驗證者簽名、 每個時間戳至可信根憑證及其合格狀態，以及 PDF 文件的簽名。 在歐盟以外地區， 合格時間戳記及報告整體的法律效力，由接收該報告的 法院或主管機關決定；該印章僅顯示報告的生成時間，並證明其內容未被篡改。

一份驗證報告無法排除 Intel TDX 模組或微程式中存在漏洞，亦無法排除對 記憶體匯流排的實體存取。無論誰控制 Phala 帳戶中的應用程式，皆可部署另一份「compose」； 它將以新的修訂版本出現，並附帶新的「compose」雜湊值。主機控制著機器 的時間來源與網路。

部署、透過 `--evidence` 進行驗證、重新啟動、作業系統映像比較、附有簽名與時間戳記的數位密封憑證，以及 銷毀等操作均已在 Phala Cloud 平台上執行；請參閱 [（2026 年 11 月 4 日執行）及](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)。

## 開始之前

1. 一個 Cloudflare 區域、其帳戶 ID，以及具備 **Cloudflare Tunnel 編輯**、 **區域讀取**和 **DNS 編輯權限的** API 憑證，由 `--cloudflare-token-file` 或 `CLOUDFLARE_API_TOKEN`提供。針對驗證者：**Cloudflare Tunnel 讀取**、**DNS 讀取**，以及針對 稽核日誌的**帳戶設定讀取**。若無網域， [快速隧道](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#quick-tunnel-without-a-domain)則無需上述任何項目。
2. 具備專用專案寫入權限的服務提供者憑證； `lock` 同樣採用：

   - Hetzner：具備讀取與寫入權限的 API 憑證；
   - DigitalOcean：具備寫入權限的個人存取憑證；
   - Linode：個人存取憑證，附帶 `linodes`, `firewall` 以及 `events` 讀寫權限；
   - Vultr：專用帳戶或子帳戶的 API 金鑰；
   - AWS：允許使用 IAM 憑證 `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` 且 `ec2:RevokeSecurityGroupIngress`.
3. 待執行的提交。發布標籤會被解析為其對應的提交，其中 `git ls-remote`； 伺服器僅會接收長度為 40 字元的提交。

## 來自控制面板

在您的電腦上，**附加說明 → 伺服器 24/7 全天候運作** 會以相同方式 `deploy` 針對 Hetzner 的設定，僅需三個 步驟：選擇歐洲或美國，貼上 Hetzner 憑證（讀寫權限），然後檢視 控制面板根據該憑證所偵測到的伺服器類型、月費、地址及版本。在您確認之前， 系統不會建立任何內容。控制面板會將每個步驟以 `deploy` 報告的狀態，接著顯示 位址、控制面板代幣及簽名金鑰指紋。若未設定網域，伺服器將取得 [快速隧道](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ；**您的伺服器 → 尋找目前的網址** 會在重新啟動後再次查詢該位址。若要在您自己的網域下設定固定位址，請開啟 **選用 · 您的專屬網域** 並新增 Cloudflare 代幣（預先準備的連結會選取「區域 讀取」、「DNS 編輯」及「Cloudflare 隧道編輯」）。

這些憑證會隨每個請求從瀏覽器分頁傳輸至同一台電腦上的 TgWitness 且不會寫入任何位置；部署記錄、經過遮蔽處理的 cloud-init、面板憑證以及 用於快速隧道的位址金鑰，皆儲存於 `deployments/NAME` 資料目錄內。 控制面板僅透過直接迴路連接向主要管理員提供此功能 （`127.0.0.1`，不允許代理或隧道標頭）；若透過網路存取控制面板，則會顯示相關指令 。版本預設為正在運行的控制面板的發行標籤，此資訊透過 GitHub API 解析取得。位置、伺服器類型與價格則來自 Hetzner 的 API： `cpx22` 若該地區有 提供，否則則採用至少 2 GB 記憶體的最低價 x86 類型。

## 無需網域的快速隧道

`--quick-tunnel` 取代 `--zone`, `--cloudflare-account` 並 `--panel-host`；無需使用 Cloudflare 帳戶或憑證：

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

在伺服器端，cloudflared 會開啟一條 [快速隧道](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) 連接到控制面板：一個隨機 `https://….trycloudflare.com` 位址，該位址會在 cloudflared 或伺服器重新啟動時變更。伺服器上的一個小型服務會將每個位址發佈至隨機的 ntfy.sh 主題，並使用僅部署目錄所持有 的金鑰進行簽名（HMAC-SHA256） （`address-key.txt`），並每三小時重複發布一次，因為 ntfy.sh 會保留貼文長達 12 小時。 `deploy` 和**「查找當前位址**」功能僅接受經簽名的貼文，因此偽造的貼文無法 將您及您的面板憑證導向他人的位址。該主題記錄於 已發布的 cloud-init 中：任何持有這些資訊的人都能讀取當前位址，而該位址仍會要求提供 面板憑證。無論何種情況，伺服器均不保留任何傳入連接埠。

驗證器沒有地址金鑰，任何讀取該主題的人都能向其發佈訊息。因此，收集器 也會發佈該地址本身，並使用其自身的 Ed25519 金鑰進行簽名；而 `verify` 會取用部署記錄中 由收集器金鑰簽名的最新發佈訊息；發佈訊息的排序依據是 ntfy.sh 接收它們的時間，而非它們聲稱的時間。 在此變更之前的收集器不會對任何內容進行簽名，而 `verify` 隨後會取用最新的貼文，並在 `statement` 檢查中表明此點；偽造的貼文 只能導致該檢查失敗，因為該地址仍必須使用收集器的金鑰進行回應。

代價為何：由於沒有 Cloudflare 帳戶會記錄快速隧道，因此 `verify` 會將 隧道、連接器及 DNS 檢查報告為不可用，結果最好也只能達到 `incomplete`（在 Phala Cloud 上，檢查則會通過：連接器在受測的 Docker Compose 配置中運行）； 供應商記錄、防火牆、簽名聲明、主機測量及安裝程式比對均 照常檢查。與參考安裝程式的位元組比對需要一個已部署的提交 版本，該版本必須已知 `--quick-tunnel`；從 0.7.0 版本檢出後，會建置網域安裝程式並回報 差異。 Cloudflare 對快速隧道不提供正常運作時間保證，允許 200 個 待處理請求，且不傳輸 Server-Sent Events，因此控制面板的即時更新（0.7.0 之後的版本） 可能無法透過快速隧道傳送，需重新載入頁面；此部分尚未進行測試。若需 確保系統穩定運作，請使用您自己的網域。

## 部署

請先查看所有即將發送的內容。 `plan` 不會向任何服務供應商或 Cloudflare 發出請求：

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

接著使用相同的選項和憑證進行部署：

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

初學者適用的伺服器類型： `cpx22` (Hetzner)， `s-1vcpu-2gb` (DigitalOcean)， `g6-standard-1` (Linode)， `vc2-1c-2gb` (Vultr)， `t3.small` (AWS)。 `--location` 以及 `--image` 預設使用各 供應商位於歐洲區域的 Ubuntu 24.04 系統。

`--repository` 從另一個 https Git 儲存庫擷取提交，且 URL 中不包含憑證 （預設 `https://github.com/phishdestroy/TgWitness.git`). `deploy` 亦接受 `--out` 指定其他部署目錄（預設 `deployments/NAME`；若目錄中已存在 部署則會被拒絕）以及 `--wait`，即等待收集器簽署聲明所需的分鐘數： 1 至 240，預設值為 20，或 60 適用於 `generic`.

指令：

1. 建立一個 Cloudflare 隧道，其入站流量會將面板主機名稱轉發至面板， 若已指定，則將見證主機名稱轉發至 `/api/witness/head` 並 `/api/assurance` 且僅限於該主機名；
2. 為這些主機名稱建立代理 CNAME 記錄，並拒絕已存在的主機名稱；
3. 建立一個沒有入站規則的提供者防火牆，並在其後方配置一台伺服器，該伺服器不使用 SSH 金鑰、 不進行備份、無控制台代理程式，且透過 cloud-init 來遮蔽 SSH、鎖定 root 權限，並安裝 `cloudflared`、精確取得該提交、驗證並啟動 TgWitness 作為 經過強化處理的 systemd 服務；
4. 等待收集器傳回的簽名聲明，並驗證該聲明是否指明此伺服器以及 此 cloud-init 的雜湊值。

`deployments/case-2026-11/` 接著包含：

| 檔案 | 目錄 | 分享？ |
| --- | --- | --- |
| `deployment.json` | ID、雜湊值、執行的 API 呼叫（方法、路徑、狀態）以及第一條已簽署的陳述 | 是的，搭配驗證器 |
| `cloud-init.redacted.yaml` | 將原始的 cloud-init 指令中的兩個機密值替換為 `REDACTED` | 是 |
| `panel-token.txt` | 面板代幣 | 否 |

服務提供者的根密碼、隧道代幣及控制面板代幣絕不會寫入 `deployment.json`。請透過您無法獨自控制的頻道（例如見證頻道或發送給收件者的訊息），發布文末列出的收集器指紋。

請透過 `https://case.example.org` 並使用面板代幣登入，操作方式參照 [帳戶指南](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/accounts/)。面板操作會記錄在已簽署的日誌中；這些並非 SSH 連線。[見證者](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/witness/)可輪詢 `https://case-witness.example.org`.

本工具不支援 SSH：若初始化失敗，收集器將永遠不會回應。請刪除伺服器並 重新部署，或使用除錯部署來找出原因。

### 使用者資料中的秘密

cloud-init 攜帶兩項機密：控制面板憑證與 Cloudflare 隧道憑證。 簽名金鑰並不包含在內；它是在伺服器上生成的。Hetzner、DigitalOcean 和 Linode 不會透過其 API 回傳使用者資料。Vultr 會將資料回傳給任何能讀取該 執行個體的金鑰，而 EC2 則透過 `DescribeInstanceAttribute`。對於 AWS，僅向驗證者提供表格中的三項 操作，絕不 `ec2:Describe*`。針對 Vultr，假設驗證者的金鑰可讀取兩者 的憑證。隧道憑證允許某人執行第二個連接器： `verify` 這會通報任何 不在伺服器上的連接器，且收集器的陳述無法以此方式偽造，因為每則陳述 都會簽署一個新的挑戰碼。若使用 `--quick-tunnel` 第二個密鑰則是位址金鑰： 任何讀取它的人都能發佈一個虛假位址，而控制面板會接受該位址。

該蒐集器的公開聲明中未提及伺服器位址及登入來源； 這兩項資訊均保留在已簽署的日誌中。

## 除錯部署與鎖定

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` 僅保留來自單一位址 或小型網路（IPv4 至多為 /24，IPv6 至多為 /48）的單一金鑰之 SSH 連線。 `KEY` 已向 服務供應商註冊：Hetzner 專案中的 SSH 金鑰名稱或 ID、DigitalOcean 團隊中的 SSH 金鑰 ID 或指紋、其個人檔案中的 SSH 金鑰已新增至 root 的 Linode 使用者名稱、 Vultr 帳戶中的 SSH 金鑰 ID，或該區域內 EC2 金鑰對的名稱。這些 選項不適用於 `generic`。此類部署將被記錄為 `debug` ，且**絕不會**被報告為 高保障等級。完成後，請執行 `sudo tgwitness-lock` 作為最後一個 SSH 連線的最後一道指令，接著：

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

防火牆會遺失所有進站規則。報告隨後會顯示何時允許 SSH 連線以及何時 被關閉；該視窗將持續顯示。

## 移除部署

`destroy` 刪除伺服器及其防火牆（透過部署標籤定位），以便 中途失敗的部署也會一併移除，接著刪除指向其 隧道的 DNS 記錄，以及隧道本身。伺服器的日誌與簽名金鑰將一併刪除：請先 匯出相關證據。紀錄將保留下來，並標記 `removed`，並附有移除操作的 API 呼叫紀錄。

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

針對 Hetzner，已實作透過 API 進行移除的功能。對於其他服務供應商 `destroy` 在刪除任何資料前， 請先在服務商控制台中指定要刪除的標籤名稱。手動安裝的 伺服器（`generic`）僅會遺失其隧道與 DNS 記錄。快速隧道部署無需 Cloudflare 憑證：其隧道僅止於伺服器，且相關貼文將於 12 小時內 從 ntfy.sh 過期。

## 任何伺服器（自我驗證）

`--provider generic` 適用於自行購買或手動安裝的伺服器。 `deploy` 建立隧道 及 DNS，並寫入 `install.sh` （私有）及 `install.redacted.sh` （用於發佈），並進入待機狀態。 將 `install.sh` 至新安裝的 Ubuntu 24.04 伺服器，並在該處執行：

```
sudo bash install.sh
```

它會記錄主機的原始狀態（登入紀錄、帳戶、 `authorized_keys`、監聽套接字、 服務、排程任務、套件）的原始狀態，安裝該提交版本，啟用主機防火牆，刪除 自身，遮蔽 SSH 並結束連線。此類伺服器的報告頂多只能算是 **「自我證明」**：無論誰執行安裝程式，在執行前都已擁有 root 權限，且驗證者無法取得 任何提供者記錄。但這仍優於來源不明的伺服器：資產清單、 安裝程式雜湊值以及後續每次登入皆經過簽名。

## 驗證

驗證者需要 `deployment.json`已發布的安裝程式、唯讀憑證，以及 最好是該提交的代碼庫副本和一份證據 ZIP：

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

驗證者會於當下向每個服務提供者及 Cloudflare 索取相關值；該記錄 僅提供需查詢的 ID。**PASS** 的退出代碼為 0，**失敗** 的退出代碼為 1，而 **檢視**、**未完成** 或 **自我驗證** 的退出代碼則為 2。 `--fingerprint` 應來自獨立的 通道；若無此通道，則僅將金鑰與操作員的記錄進行比對。 `python verify.py` 仍會驗證證據 ZIP 本身，如同 [證據](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/) 一樣。

供應商操作分為以下類別：建立及在建立後 30 分鐘內啟動的操作均通過審核； 控制台、救援、密碼重設、重建、ISO、映像檔、快照、備份、系統管理員、 EC2 實例連線及防火牆開啟等操作若失敗；電源操作及任何未預期的 操作則會被標記待審查。未知操作絕不會在未經通知的情況下通過審核。

## 證據移交報告

`--report report.md` 撰寫 Markdown 報告，並 `report.json` 其旁：

1. 結果、收集器金鑰指紋、部署、提供者、提交、伺服器、防火牆、隧道；
2. 每項檢查及其狀態與來源（供應商 API、Cloudflare API、收集器聲明、 證據日誌）；
3. 提供者日誌，其中包含每項操作的評估結果，以及（若提供者有記錄的話）執行者；
4. Cloudflare 端點，用於儲存隧道連線、設定及稽核日誌；
5. 經簽署的收集者聲明；
6. 該報告闡明的事項與未闡明的事項；
7. 用於重現該結果的指令，以及所有輸入檔案的 SHA-256。

提交報告、 `report.json`, `deployment.json`、已發布的安裝程式以及 證據 ZIP。請盡早製作報告：服務供應商的日誌僅會保留有限時間。

## Cloudflare 作為外部見證者

此處的所有功能皆為選用。即使沒有 Cloudflare 帳戶，伺服器仍可運作，且目前有兩項 功能可正常運作：

| 什麼 | 功能展示 | 在 TgWitness |
| --- | --- | --- |
| 快速隧道或您自己的網域隧道 | 該面板僅能透過隧道存取 | 伺服器精靈，請參閱上文 |
| drand 中繼站 `drand.cloudflare.com` | drand 輪次結束後的記錄比這份文件更新：這份日誌是邊進行邊撰寫的 | 證據模式、**更多見證者**、無帳戶（[格式](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)） |
| 隧道狀態通知 | 當隧道中斷時，透過電子郵件或來自 Cloudflare 的 Webhook 通知 | 請在 Cloudflare 控制台中進行設定 |
| Gateway DNS（`--gateway-dns`，或在設定精靈中稱為 **Cloudflare Gateway DNS**） | 伺服器查詢的每個名稱，皆由 Cloudflare 透過 TLS 回應；Hetzner 防火牆不允許 DNS 連通其他任何目標；閘道器 (Gateway) 政策是否能重寫回應內容 | Hetzner，免費的「零信任」方案，無需網域； `verify` 檢查防火牆、位置、日誌記錄、政策、伺服器查詢及稽核日誌；證據模式會將日誌複製到日誌簿中 |
| 與 Cloudflare 的閘道：伺服器上僅有一台 Cloudflare One 客戶端，以及一個僅允許 Cloudflare 通行的出站防火牆 | 伺服器建立的每項連線，而不僅是 DNS | 尚未建置 |
| 在面板前方存取 | 誰在何時登入該面板 | 尚未建置：需自行準備網域 |
| SSH 命令記錄 | 除錯會話中的每個指令 | 尚未建置 |

Logpush 會將 Cloudflare 的副本保留在 R2 中，這是一項企業級功能：在免費 方案中，Cloudflare 會回應 `logpush is not enabled for this account`。其閘道器日誌在該處保留 24 小時，因此「證據模式」會將其複製到簽名日誌中（**Cloudflare 閘道器的日誌，記錄 此伺服器的 DNS**查詢，這是一個具備「帳戶分析讀取權限」的唯讀憑證）。

若未實施「零信任」方案，每個帳戶僅有一個 DNS 位置。當 Cloudflare 拒絕其他位置時， 伺服器會共用現有的位置，並透過其位址來區分查詢；該篩選機制 同樣需要「零信任 PII 讀取」權限，且 `destroy` 仍會留下共用位置。單一日誌查詢的範圍 最多為三小時，因此複製並 `verify` 讀取作業將以三小時為單位進行。

Gateway DNS 涵蓋系統解析器。透過 443 埠的 HTTPS DNS 連線至其他解析器，以及 連線至未經任何處查詢的地址（例如 Telegram 的資料中心），均不會 記錄於其日誌中。

Cloudflare 無法窺見 Telegram 的加密內容、該 Telegram 帳戶上的其他裝置 （「證據模式」的裝置清單是從 Telegram 端記錄下來的），亦無法窺見服務供應商的虛擬化平台。

## 閱讀部署結果

對於一般虛擬機器，服務供應商負責管理主機基礎架構，並會同步核對 本地資源清單與供應商紀錄。針對 Intel TDX，驗證者還會額外檢查 硬體規格、收集器綁定、編組及作業系統測量值。請閱讀各項 結果，以確認哪些檢查通過或無法取得。

歷史防火牆詳情取決於服務供應商；Linode 會保留規則版本。 [驗證](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/verification/)記錄列出了已測試的部署及剩餘的即時 檢查，而[驗證範圍](https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/evidence/#verification-scope)則將這些環境 檢查與存檔的取得及完整性連結起來。
