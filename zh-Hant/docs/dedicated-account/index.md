# 請使用獨立的帳戶。切勿使用您的主要帳戶。

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/dedicated-account/

連接帳戶前請先閱讀

我們建議您不要使用主要帳戶，這絕非玩笑，而是現實。

主帳戶

- 您應用程式的雜湊值：99% 已登出
- 僅因「低信任度」而遭封禁的情況屢見不鮮
- 使用它真是個極其愚蠢的主意

公開對中的額外帳戶

- 透過這些組合註冊的帳戶已超過一百萬個
- 這些配對已運作超過 5 年
- 透過這些介面，任何人都無法窺見您的任何資訊

01

## 為何不使用您的主要帳號

這是準確的資訊。我們確切知道這些問題的陷阱所在。

1. ### 您應用程式的雜湊值：99% 已登出

   若從您無權存取的帳戶登入 my.telegram.org 以取得應用程式雜湊值，隨後透過該應用程式雜湊值發送任何請求，則該帳戶有 99% 的機率已被登出。您可以自行驗證。
2. ### 僅因「低信任度」而遭封禁的情況屢見不鮮

   帳戶被封禁純粹是因為 Telegram 不信任它們，且此類封禁情況屢見不鮮。您也可以自行查證。使用自己的帳戶實在是個極其愚蠢的主意。
3. ### 已複製的會話金鑰可被撤銷

   若同時在 Telegram Desktop 和 TgWitness 中執行已匯入的 TData/會話金鑰，可能會觸發 `AUTH_KEY_DUPLICATED` 錯誤。Telegram 會使該授權失效，因此兩份副本均需重新登入。即使使用專用帳戶也無法避免此情況。

   請完全退出原始客戶端，並在使用其匯入的會話期間保持該客戶端關閉。若需並行使用，請透過手機或 QR 碼登入 TgWitness 以建立獨立的授權；其他已獲得獨立授權的客戶端可保持登入狀態。

   [請閱讀會話匯入警告](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh-Hant#session-warning)

Telegram 文件

- [登出錯誤：AUTH_KEY_UNREGISTERED、SESSION_REVOKED](https://core.telegram.org/api/errors)
- [建立您自己的應用程式雜湊值：取得 api_id](https://core.telegram.org/api/obtaining_api_id)

02

## 為何 TgWitness 透過公開的應用程式雜湊值／應用程式 ID 配對運作

這就是為什麼我們以公開的應用程式雜湊值／應用程式 ID 配對為基礎建構 TgWitness。依我們的邏輯，使用這些配對被封禁的機率較低：已有超過一百萬個 Telegram 帳號透過這些配對註冊，且許多不同的程式皆能透過它們運作。 依我們的邏輯，這比直接使用個人應用程式哈希更為穩妥：這些組合肯定已存在超過 5 年。

### 您自己的新密鑰對

由該帳號於 my.telegram.org 建立。

- 約 99% 的帳戶已登出
- 一個新應用程式，一個帳戶

### 池中的公開金鑰對

這與許多程式所使用的組合相同。

- 註冊帳戶數已突破一百萬
- 許多不同的程式
- 擁有 5 年以上工作經驗

### 為何透過這對裝置，無人能窺見您的任何資訊

- #### 該對組合是一個名稱，而非金鑰

  當程式連線或請求登入碼時，Telegram 會要求提供 API ID 和 API 雜湊值。這些資訊僅用於識別應用程式，並不會授予任何帳戶的存取權限；Telethon 的文件中指出，一組 API ID 與 API 雜湊值可適用於任何電話號碼。
- #### 您的會話金鑰絕不會離開您的伺服器

  登入時，系統會透過您的 TgWitness 與 Telegram 之間的 Diffie–Hellman 交換機制生成授權金鑰；該金鑰本身絕不會被傳送出去。根據 Telegram 的文件說明：授權完成後，該金鑰將與使用者綁定，且所有使用此金鑰的呼叫皆以該使用者身分執行。其他擁有相同密鑰對的程式各有其專屬金鑰，無法使用您的金鑰。
- #### 流量將使用您的金鑰進行加密

  每個請求與回應皆使用該會話的授權金鑰進行加密，而非使用 API 雜湊值。即使知曉 API 雜湊值，也無法解密任何內容。
- #### 該對的擁有者無法看到任何內容

  Telegram 沒有任何方法可根據 API ID 列出帳戶、會話或訊息。一對帳戶的所有者僅能在 my.telegram.org 上查看其應用程式設定。
- #### 僅您的帳戶能識別該應用程式是哪一款

  您個人帳戶的「設定 → 裝置」中，會列出每個連線的應用程式名稱、API ID、裝置、IP 位址及日期。此清單僅您本人可見，不會提供給任何其他人。

Telegram 文件

- [使用者授權：密鑰即使用者](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [建立授權金鑰](https://core.telegram.org/mtproto/auth_key)
- [MTProto 加密](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [會話記錄的內容](https://core.telegram.org/constructor/authorization)
- [取得 api_id](https://core.telegram.org/api/obtaining_api_id)
- [Telegram 應用程式的開源程式碼](https://telegram.org/apps#source-code)

資源庫與討論區

- [Telethon：登入](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele：官方應用程式 API](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow：是否應將 api_hash 保密？](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### 其他程式中的相同字串對 7

這對官方 Telegram 應用程式是公開的，並已內建於許多獨立程式和函式庫中：

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  論壇上公布的官方應用程式配對清單，供註冊帳戶使用

03

## 建立額外帳戶的方法

Telegram 帳戶需要一個可接收登入驗證碼的電話號碼。請根據該帳戶的預期使用期限來選擇。

- 最佳選擇

  ### 預付 SIM 卡或 eSIM

  ********

  最後

  只要您保持餘額充足

  請注意

  最可靠的方式：Telegram 最能接受真實的行動電話號碼。電信業者收回的號碼會分配給其他人。
- ### 虛擬號碼應用程式

  ********

  最後

  雖然該應用程式會保留數量

  請注意

  Telegram 可能會拒絕虛擬號碼、不發送驗證碼，或立即限制新帳戶的使用；部分應用程式會收回未使用的號碼。
- ### 租用編號

  ********

  最後

  租賃期間

  請注意

  當此號碼用完時，將轉給下一位客戶。
- ### 一次性啟用

  ********

  最後

  一段程式碼

  請注意

  該號碼會立即返回號碼池，通常會附帶先前持有者的使用紀錄。請務必在執行任何其他操作之前，先設定雲端密碼。

日後持有該號碼者可請求登入碼。雲端密碼（兩步驟驗證）可阻止其登入；若未提供該密碼，該帳號將歸屬於該號碼的下任持有者。

Telegram 文件

- [垃圾訊息常見問題：虛擬號碼與前任持有者](https://telegram.org/faq_spam)
- [兩步驟驗證](https://core.telegram.org/api/srp)

### 租用的 +888 號碼（Fragment）

部分市場平台及服務提供透過 Fragment 臨時租用 Telegram 官方 +888 號碼的服務。

預估價格：每日 20 美元。

- 您可直接在 Telegram Web 或 Telegram Desktop 上註冊帳號。
- 您可以刪除該號碼下的帳戶並建立新帳戶。
- 此類帳號通常面臨較少的反詐欺檢查，但並不提供豁免權或特殊特權。

該號碼並非您所有。租用期滿後，所有者可取回該號碼。請立即設定雲端密碼，且切勿將此帳號視為長期使用。

自行持有 +888 號碼，或使用您所掌控的預付 SIM 卡，仍是較為可靠的作法。

### 來自交易平台的現成帳號

部分交易平台（例如 G2G 或 Z2U）販售現成的 Telegram 帳號——包括新帳號、已使用一段時間的帳號，或附帶會話檔案的帳號。

- [G2G：Telegram 帳號列表](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U：Telegram 帳號列表](https://www.z2u.com/telegram/accounts-5-15140)

切勿使用您的主要帳號！透過此方式建立的專用帳號，仍比將您的主要 Telegram 帳號加入 TgWitness 更為安全。

#### 購買前的警告

- 此舉違反 Telegram 的《服務條款》。
- 許多帳號屬批量註冊（自動註冊）或歷史背景不明。
- 部分賣家可能仍保有恢復權限。
- 來自此類市場的帳號事後經常會遭到封禁或限制。
- 請避免使用那些公開販售帳戶竊取工具、釣魚工具或明顯為盜取帳戶的市集。
- 從公開販售釣魚工具、竊取程式、盜取的會話或帳戶的平台上購買帳戶——即使是標榜「自動註冊」的帳戶——不僅違反 Telegram 的《服務條款》，也違反大多數國家的法律。此舉日後可能導致您的證據失效。請謹慎選擇。

#### 若您使用此選項

1. 請將此帳號視為一次性帳號。
2. 請立即終止所有其他連線、設定雲端密碼，並變更帳戶恢復方式。
3. 請使用 2 至 3 個來自不同服務供應商的帳戶，或您自行註冊的帳戶。

**Premium、刪除與七天延遲**

若該帳號已啟用 Premium 服務，即使有人取得該電話號碼，也無法立即刪除該帳號。您將收到通知，並有七天的時間在帳號被刪除前採取行動。

此事至關重要，因為您的調查取決於該帳號：您仍有時間準備替代方案。

**新帳號與 API 憑證**

若您透過自行註冊的新帳號（使用簡訊服務提供的號碼）取得並使用專屬的 api_id/api_hash，該帳號將在首次 API 請求或會話授權時被登出。規劃調查時請務必謹記此點。

04

## 建立帳戶

從一個數字到首則記錄的聊天內容。

1. ### 取得一個數字

   若帳戶需長期使用，請選用預付 SIM 卡或 eSIM；若僅需短期作業，則可選擇租用或一次性啟用方案。相關服務列表如下。
2. ### 請使用與您的主要帳戶不同的帳戶進行註冊

   請在官方 Telegram 應用程式中，透過獨立裝置、模擬器或手機設定檔進行註冊，切勿與您的主要帳戶並存。
3. ### 使用雲端密碼進行鎖定

   請立即設定一個僅用於此處的雲端密碼及備用電子郵件。
4. ### 關閉隱私設定

   電話號碼 **「無人**」，「透過我的號碼找到我」；「**我的聯絡人**」、「最後一次上線」、「個人頭像」及「個人簡介」；**「無人」**或「**我的聯絡人**」；請關閉聯絡人同步功能。
5. ### 防止其自動銷毀

   請將帳戶自動銷毀設定為最長期限，以免 TgWitness 停止運作時導致您失去該帳戶。
6. ### 賦予其中立的形象

   請勿使用您其他帳戶的名稱、照片、使用者名稱或個人簡介，亦請勿提供個人聯絡資訊。
7. ### 讓它預熱一下

   起初每天加入幾個聊天室即可。新帳號若過於倉促，將首先受到限制。
8. ### 切勿與機器人分享任何資訊

   切勿為任何機器人點擊「分享電話號碼」或「分享位置」。請透過該裝置上的 VPN 或代理伺服器開啟連結及 Mini Apps。
9. ### 將其連接到 TgWitness

   在您自己的工作區中，透過「**帳戶 → QR 碼**」進行連線，然後點選「**來源 → 調查模式」**。應用程式是您採取行動的地方，TgWitness 則是記錄的載體。

Telegram 文件

- [兩步驟驗證](https://core.telegram.org/api/srp)
- [隱私權設定](https://core.telegram.org/api/privacy)
- [帳戶自動銷毀](https://core.telegram.org/method/account.setAccountTTL)

05

## 服務編號

起始選項。國家、價格以及 Telegram 是否允許變更號碼等資訊經常變動；付款前請務必確認。

### 預付 SIM 卡與 eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - 預付

  PayGo 方案，價格非常便宜
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - 預付
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - 預付
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - 預付
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### 虛擬號碼應用程式 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  僅限美國；註冊需提供美國電話號碼
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  若未使用該號碼，系統將收回該號碼
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - 其他國家
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - 付費

  附帶試用期
- [Hushedhushed.com](https://hushed.com)

  - 許多國家
  - 付費

  廉價
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  應用程式中的歐洲手機號碼
- [Sonetelsonetel.com](https://sonetel.com)

  - 許多國家
  - 免費號碼
- [Zadarmazadarma.com](https://zadarma.com)

  - 許多國家

  虛擬號碼

### 租用與啟用次數 12

租用服務會保留號碼數週或數月。一次性啟用僅提供單一代碼：請於註冊後立即設定雲端密碼。

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - 租賃
  - 啟用
- [SMSPVAsmspva.com](https://smspva.com)

  - 租賃
  - 啟用
- [5SIM5sim.net](https://5sim.net)

  - 租賃
  - 啟用
- [SMSPoolsmspool.net](https://www.smspool.net)

  - 租賃
  - 一次性
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - 租賃
  - 啟用
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - 租賃
  - 啟用
- [JuicySMSjuicysms.com](https://juicysms.com)

  - 租賃
  - 啟用
- [365SMS365sms.org](https://365sms.org)

  - 租賃
  - 啟用
- [SIMSMSsimsms.org](https://simsms.org)

  - 租賃
  - 啟用
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - 一次性
- [SMS-MANsms-man.com](https://sms-man.com)

  - 一次性
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - 一次性
