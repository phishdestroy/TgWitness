# 请使用独立账户，切勿使用您的主账户。

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/dedicated-account/

连接账户前请先阅读

我们建议您不要使用主账号，这绝非玩笑，而是现实。

主账户

- 使用您自己的应用哈希，99% 的账户都会被注销
- 仅因“信任度低”而导致账号被封的情况屡见不鲜
- 使用你的主账号是一个非常愚蠢的主意

基于公共 API ID/API 哈希对的额外账户

- 已有超过一百万个账户通过这些 API ID/API 哈希对注册
- 这些 API ID/API 哈希对已持续有效超过 5 年
- 任何人都无法通过这些 API 对查看您的任何数据

01

## 为什么绝对不能使用您的主账号

这是准确的信息。我们清楚地知道这些问题存在哪些隐患。

1. ### 使用您自己的应用哈希，99% 的账户都会被注销

   如果使用一个你无权访问的账户登录 my.telegram.org 以获取应用哈希，随后通过该应用哈希发送任何请求，则该账户被注销的概率高达 99%。你可以亲自验证一下。
2. ### 仅因“信任度低”而导致账号被封的情况屡见不鲜

   账号被封禁仅仅是因为 Telegram 不信任它们，此类封禁情况十分常见。你也可以自行核实这一点。使用自己的账号确实是个极其愚蠢的主意。
3. ### 已复制的会话密钥可以被撤销

   在 Telegram Desktop 和 TgWitness 中同时运行导入的 TData/会话密钥可能会触发 `AUTH_KEY_DUPLICATED` 错误。Telegram 会使该授权失效，因此两个副本都需要重新登录。使用专用账户也无法避免此情况。

   请完全退出原始客户端，并在使用其导入的会话期间保持该客户端关闭状态。如需并行使用，请通过手机或二维码登录 TgWitness 以建立独立的授权；其他已单独授权的客户端可保持登录状态。

   [请阅读会话导入警告](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=zh#session-warning)

Telegram 文档

- [注销错误：AUTH_KEY_UNREGISTERED、SESSION_REVOKED](https://core.telegram.org/api/errors)
- [创建您自己的应用哈希：获取 api_id](https://core.telegram.org/api/obtaining_api_id)

02

## 为什么 TgWitness 通过公开的应用哈希和应用 ID 对来工作

正因如此，我们基于公开的应用哈希/应用 ID 对构建了 TgWitness。按照我们的逻辑，使用这些对被封禁的可能性较低：已有超过一百万个 Telegram 账户通过这些对注册，且许多不同的程序都通过它们运行。 依我们的逻辑，这比直接使用个人应用哈希更稳妥：这些哈希-ID 对肯定已经存在了 5 年以上。

### 您自己的新 API ID/API 哈希对

由该账户在 my.telegram.org 上创建。

- 其中约 99% 的账户会被自动注销
- 一个新应用，一个账户

### 来自池中的公共 API ID/API 哈希对

这与许多程序所使用的 API ID/API hash 对相同。

- 注册账户已超过一百万个
- 多种不同的程序
- 这些 API 对已稳定运行 5 年以上

### 为什么没有人能通过这些 API 对查看您的任何数据

- #### 该 API 配对是一个名称，而非键

  当程序连接或请求登录码时，Telegram 会要求提供 API ID 和 API 哈希。这些信息用于识别应用程序，但不会授予任何账户的访问权限；Telethon 的文档指出，一组 API ID 和 API 哈希可适用于任何手机号码。
- #### 您的会话密钥绝不会离开您的服务器

  登录时，您的 TgWitness 与 Telegram 之间会通过迪菲-赫尔曼（Diffie–Hellman）密钥交换生成一个授权密钥；该密钥本身绝不会被发送出去。根据 Telegram 的文档说明：授权后，该密钥将与用户绑定，使用此密钥的每次调用均以该用户身份执行。其他拥有相同密钥对的程序各有自己的密钥，无法使用您的密钥。
- #### 数据传输使用您的密钥进行加密

  每个请求和响应均使用会话授权密钥进行加密，而非 API 哈希值。仅知晓 API 哈希值无法解密任何内容。
- #### API ID/API hash 对的所有者无法看到任何内容

  Telegram 没有通过 API ID 列出账户、会话或消息的方法。账户所有者只能在 my.telegram.org 上查看其应用设置。
- #### 只有您的账户能看到这是哪个应用

  在“设置”→“您自己的账户设备”中，会列出每个会话的应用名称、API ID、设备、IP 地址和日期。除您本人外，任何人都无法查看此列表。

Telegram 文档

- [用户授权：密钥将与用户绑定](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [创建 MTProto 授权密钥](https://core.telegram.org/mtproto/auth_key)
- [MTProto 加密](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Telegram授权（会话）条目包含的内容](https://core.telegram.org/constructor/authorization)
- [获取 api_id](https://core.telegram.org/api/obtaining_api_id)
- [Telegram 应用的开源代码](https://telegram.org/apps#source-code)

库和讨论帖

- [Telethon：登录 Telegram](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele：官方应用的 API 凭据](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow：是否应将 api_hash 保密？](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### 其他程序中相同的 API ID/API 哈希对 7

官方 Telegram 应用的 API ID/API 哈希对是公开的，并已集成到许多独立程序和库中：

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

  一篇列出了官方 Telegram 应用的 API ID/API hash 对的论坛帖子，发布目的是用于注册账户

03

## 创建额外账户的方法

Telegram 账号需要一个用于接收登录验证码的手机号码。请根据该账号的预期使用时长进行选择。

- 最佳选择

  ### 预付费 SIM 卡或 eSIM

  ********

  有效期有多长

  只要您保持余额充足

  请注意

  最可靠的方法：Telegram 最能接受真实的手机号码。运营商收回的号码会被分配给其他人。
- ### 一款提供虚拟电话号码的应用程序

  ********

  有效期有多长

  只要该应用保留该手机号码

  请注意

  Telegram 可能会拒绝虚拟号码、不发送验证码，或立即限制新账户的使用；某些应用会收回未使用的号码。
- ### 租用电话号码

  ********

  有效期有多长

  关于租赁期限

  请注意

  当该号码用完后，将分配给下一位客户。
- ### 一次性激活

  ********

  有效期有多长

  仅需一个登录码

  请注意

  该号码会立即返回号码池，通常附带之前所有者的使用记录。请务必在进行其他操作之前先设置云端密码。

日后持有该号码的人可以请求登录码。云密码（两步验证）可阻止其登录；若未输入该密码，该账户将归属于该号码的下一任持有者。

Telegram 文档

- [垃圾信息常见问题解答：虚拟号码及其前任所有者](https://telegram.org/faq_spam)
- [两步验证](https://core.telegram.org/api/srp)

### 租赁的 +888 号码（Fragment）

部分市场和平台提供通过 Fragment 临时租用 Telegram 官方 +888 号码的服务。

预计价格：每天 20 美元。

- 您可以在 Telegram Web 或 Telegram Desktop 中直接注册账户。
- 您可以删除该号码下的账户并创建新账户。
- 此类账号通常面临较少的反欺诈审查，但并不因此享有豁免权或特殊特权。

该账号不属于您。租赁期满后，所有者可将其收回。请立即设置云密码，且不要将该账号视为长期使用。

自行持有 +888 号码或使用您控制的预付费 SIM 卡仍然更为可靠。

### 来自交易平台的现成账户

部分交易平台（例如 G2G 或 Z2U）出售现成的 Telegram 账号——包括新账号、老账号或附带会话文件的账号。

- [G2G：Telegram 账号列表](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U：Telegram 账号列表](https://www.z2u.com/telegram/accounts-5-15140)

切勿使用您的主账号！通过此方式创建的专用账号，仍比将您的主要 Telegram 账号绑定到 TgWitness 更为安全。

#### 购买前的警告

- 这违反了 Telegram 的《服务条款》。
- 许多账号属于批量注册（自动注册）或历史信息不明。
- 部分卖家可能仍持有恢复权限。
- 来自此类市场的账号往往会在后期遭到封禁或限制。
- 请避免使用公开销售账号窃取工具、钓鱼工具或明显为盗取账号的市场平台。
- 从公开销售钓鱼工具、窃取工具、被盗会话或账户的平台上购买账户——即使是标榜为“自动注册”的账户——不仅违反了 Telegram 的《服务条款》，也违反了大多数国家的法律。这可能会导致您的证据日后失效。请谨慎选择。

#### 如果您使用此选项

1. 将该账号视为一次性账号。
2. 请立即结束所有其他会话，设置云密码并更改恢复方式。
3. 请使用来自不同服务商或您自行注册的 2–3 个账户。

**Premium、删除及七天延迟**

如果该账号开通了 Premium 服务，即使有人获得了该手机号码的访问权限，也无法立即删除该账号。您会收到通知，并在账号被删除前有七天的处理时间。

这一点至关重要，因为您的调查工作依赖于该账号：您还有时间准备一个替代账号。

**新账户和 API 凭据**

如果您通过短信服务获取的号码注册了新账户，并从中获取和使用自己的 api_id/api_hash，则该账户将在首次 API 请求或会话授权时被强制注销。在规划调查时请务必牢记这一点。

04

## 创建账户

从获取手机号码到记录第一条聊天记录。

1. ### 获取电话号码

   若账户需长期使用，建议选用预付费 SIM 卡或 eSIM；若仅用于短期任务，则可选择租赁或一次性激活。相关服务如下所示。
2. ### 请使用与主账户不同的账户注册

   请在官方 Telegram 应用中，通过另一台设备、模拟器或手机配置文件进行注册，切勿与您的主账户在同一设备上操作。
3. ### 使用云密码保护该账号

   请立即设置一个仅用于此处的云密码和恢复邮箱。
4. ### 限制该账号的隐私设置

   电话号码：**无人**，通过号码查找我；**我的联系人**、最后上线时间、个人头像和简介：**无人**或**我的联系人**；关闭联系人同步。
5. ### 防止账号自动销毁

   请将账户自动销毁时限设置为最长，这样即使 TgWitness 停止运行，您的账户也不会因此丢失。
6. ### 为该账号设置中性的个人资料

   不包含您其他账户的姓名、照片、用户名或个人简介，也不包含个人联系人信息。
7. ### 让新账号进行预热

   起初，每天只加入几个聊天群。新账号若操之过急，往往会率先受到限制。
8. ### 不与机器人共享任何信息

   切勿点击机器人上的“分享电话号码”或“分享位置”按钮。请通过该设备上的 VPN 或代理打开链接和迷你应用。
9. ### 将该账户连接到 TgWitness

   在您自己的工作区中，通过**“账户”→“二维码**”进行连接，然后点击**“来源”→“调查模式”**。该应用是您操作的场所，TgWitness 则是记录工具。

Telegram 文档

- [两步验证](https://core.telegram.org/api/srp)
- [隐私设置](https://core.telegram.org/api/privacy)
- [账户长期闲置时的自动销毁机制](https://core.telegram.org/method/account.setAccountTTL)

05

## 电话号码服务

以下是可供参考的起始选项。国家/地区、价格以及 Telegram 是否接受特定号码等信息经常变化，因此请在付款前确认。

### 预付费 SIM 卡和 eSIM 11

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
  - 预付费

  PayGo 套餐，价格非常便宜
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - 预付费
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - 预付费
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - 预付费
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### 提供虚拟电话号码的应用程序 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  仅限美国；注册需提供美国电话号码
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  若未使用该编号，系统将收回该编号
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
  - 其他国家
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
  - 付费服务

  附带试用期
- [Hushedhushed.com](https://hushed.com)

  - 许多国家
  - 付费服务

  低价
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

  应用程序中的欧洲手机号码
- [Sonetelsonetel.com](https://sonetel.com)

  - 许多国家
  - 免费号码
- [Zadarmazadarma.com](https://zadarma.com)

  - 许多国家

  虚拟电话号码

### 电话号码租赁和一次性激活 12

租用电话号码可让您在数周或数月内持续使用该号码。一次性激活会生成一个登录验证码：请在注册后立即设置云端密码。

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - 号码租赁
  - 一次性激活
- [SMSPVAsmspva.com](https://smspva.com)

  - 号码租赁
  - 一次性激活
- [5SIM5sim.net](https://5sim.net)

  - 号码租赁
  - 一次性激活
- [SMSPoolsmspool.net](https://www.smspool.net)

  - 号码租赁
  - 一次性激活
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - 号码租赁
  - 一次性激活
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - 号码租赁
  - 一次性激活
- [JuicySMSjuicysms.com](https://juicysms.com)

  - 号码租赁
  - 一次性激活
- [365SMS365sms.org](https://365sms.org)

  - 号码租赁
  - 一次性激活
- [SIMSMSsimsms.org](https://simsms.org)

  - 号码租赁
  - 一次性激活
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - 一次性激活
- [SMS-MANsms-man.com](https://sms-man.com)

  - 一次性激活
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - 一次性激活
