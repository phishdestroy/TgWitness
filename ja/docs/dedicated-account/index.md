# 別のアカウントを使用してください。メインのアカウントは絶対に使用しないでください。

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/dedicated-account/

アカウントを連携する前に必ずお読みください

メインアカウントを使用しないようお勧めするのは、冗談ではありません。これは現実です。

メインアカウント

- ご自身のアプリのハッシュ：99%がログアウト済み
- 信頼度が低いという理由だけで利用停止処分が下されるケースは頻繁にあります
- これを使用するのは、実に愚かな考えです

パブリックペア上の追加アカウント

- これらのペアを通じて登録されたアカウントは100万件を超えています
- このペアは5年以上稼働しています
- これらを通じて、あなたの情報は誰にも見られることはありません

01

## メインアカウントではなく、こちらをご利用ください

これは正確な情報です。これらの問題の落とし穴がどこにあるか、私たちは正確に把握しています。

1. ### ご自身のアプリのハッシュ：99%がログアウト済み

   アクセス権のないアカウントから my.telegram.org にログインしてアプリハッシュを取得し、そのアプリハッシュを介してリクエストを行うと、そのアカウントがログアウトされる確率は 99% になります。ご自身で確認してみてください。
2. ### 信頼度が低いという理由だけで利用停止処分が下されるケースは頻繁にあります

   アカウントが凍結されるのは、単にTelegramがそのアカウントを信頼していないためであり、そのような凍結は頻繁に発生しています。この点についてもご自身で確認できます。ご自身のアカウントを使用するのは、実に愚かな考えです。
3. ### コピーされたセッションキーは失効させることができます

   インポートした TData/セッションキーを Telegram Desktop と TgWitness で同時に実行すると、`AUTH_KEY_DUPLICATED` が発生する可能性があります。Telegram はその認証を無効にするため、両方のコピーで新たにログインする必要があります。専用のアカウントを作成しても、これを防ぐことはできません。

   元のクライアントを完全に終了させ、インポートしたセッションを使用している間は閉じたままにしておいてください。並行して使用する場合は、電話またはQRコードでTgWitnessにサインインして別の認証を作成してください。他の個別に認証されたクライアントは、サインインしたままにしておくことができます。

   [セッションインポートに関する警告をお読みください](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ja#session-warning)

Telegramのドキュメント

- [ログアウト時のエラー：AUTH_KEY_UNREGISTERED、SESSION_REVOKED](https://core.telegram.org/api/errors)
- [独自のアプリハッシュの作成：api_idの取得](https://core.telegram.org/api/obtaining_api_id)

02

## TgWitnessがパブリックなアプリハッシュ／アプリIDのペアを通じて機能する理由

そのため、私たちはTgWitnessをパブリックなアプリハッシュ／アプリIDのペアに基づいて構築しました。私たちの考えでは、これらを使用することで利用停止処分を受ける可能性は低くなります。100万以上のTelegramアカウントがこれらのペアを通じて登録されており、多くの異なるプログラムがこれらを通じて動作しています。 私たちの考えでは、これは個人のアプリハッシュを直接扱うよりも優れています。これらのペアは、確実に5年以上も稼働し続けているからです。

### ご自身で作成した新しいペア

my.telegram.org上のアカウントから作成されました。

- 約99％のアカウントがログアウトしました
- 1つの新しいアプリケーションにつき、1つのアカウント

### プールの公開鍵ペア

多くのプログラムで使用されているのと同じペアです。

- 登録アカウント数は100万件を超えています
- さまざまなプログラム
- 5年以上の実務経験

### なぜ、これらのペアを通じてあなたの情報は誰にも見られないのか

- #### このペアは名前であり、鍵ではありません

  Telegramは、プログラムが接続する際やログインコードを要求する際に、API IDとAPIハッシュを求めます。これらはアプリケーションを識別するものであり、いかなるアカウントへのアクセス権も付与しません。Telethonのドキュメントには、1組のペアでどの電話番号でも利用可能であると記載されています。
- #### セッションキーは、サーバーの外に出ることはありません

  ログインすると、TgWitnessとTelegram間のディフィー・ヘルマン交換によって認証キーが生成されますが、キー自体は決して送信されません。Telegramのドキュメントによると、認証後、キーはユーザーに関連付けられ、このキーを使用したすべての呼び出しはそのユーザーとして実行されます。同じ鍵ペアを持つ他のプログラムは独自のキーを持っており、あなたのキーを使用することはできません。
- #### 通信はお客様の鍵で暗号化されます

  すべてのリクエストと応答は、APIハッシュではなく、セッションの認証キーを使用して暗号化されます。APIハッシュを知っていても、何も復号化することはできません。
- #### ペアの所有者には何も表示されません

  Telegramには、API IDごとにアカウント、セッション、メッセージを一覧表示する機能はありません。ペアの所有者は、my.telegram.org上で自身のアプリ設定のみを確認できます。
- #### どのアプリであるかは、ご自身のアカウントでのみ確認できます

  ご自身のアカウントの「設定」→「デバイス」には、各セッションのアプリ名とAPI ID、デバイス、IPアドレス、および日付が一覧表示されます。この一覧は、ご本人以外には表示されません。

Telegramのドキュメント

- [ユーザー認証：鍵がユーザーそのものとなります](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [認証キーの作成](https://core.telegram.org/mtproto/auth_key)
- [MTProto暗号化](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [セッション記録に含まれる内容](https://core.telegram.org/constructor/authorization)
- [api_id の取得](https://core.telegram.org/api/obtaining_api_id)
- [Telegramアプリのオープンソースコード](https://telegram.org/apps#source-code)

ライブラリおよびディスカッション

- [Telethon：ログイン](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele：公式アプリAPI](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow：api_hashは秘密にしておくべきでしょうか？](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### 他のプログラムにおける同様のペア 7

公式のTelegramアプリは公開されており、多くの独立したプログラムやライブラリに組み込まれています：

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

  アカウント登録用に公開された、公式アプリペアのフォーラム一覧

03

## 追加アカウントを作成する方法

Telegramアカウントには、ログインコードを受信するための電話番号が必要です。アカウントの有効期間に応じて選択してください。

- 最適な選択

  ### プリペイドSIMまたはeSIM

  ********

  最後

  残高を常に補充しておいてください

  ご注意ください

  最も信頼性が高いのは、Telegramが実際の携帯電話番号を最優先で受け入れる点です。通信事業者が回収した番号は、他の誰かに割り当てられます。
- ### 仮想番号アプリ

  ********

  最後

  このアプリは数を保持していますが

  ご注意ください

  Telegramは、仮想番号の割り当てを拒否したり、認証コードを送信しなかったり、新規アカウントの利用を直ちに制限したりする場合があります。また、一部のアプリでは、使用されていない番号を回収することがあります。
- ### レンタル番号

  ********

  最後

  レンタル期間

  ご注意ください

  終了すると、その番号は次の顧客に割り当てられます。
- ### 1回限りの有効化

  ********

  最後

  1つのコード

  ご注意ください

  その番号は直ちにプールに戻され、多くの場合、過去の所有者の履歴が付随しています。何よりも先に、クラウドのパスワードを設定してください。

後でその番号を所有する人は誰でも、ログインコードをリクエストできます。クラウドパスワード（2段階認証）があれば、その人がログインするのを防ぐことができます。それがなければ、そのアカウントは番号の次の所有者に帰属することになります。

Telegramのドキュメント

- [スパムに関するFAQ：仮想番号と以前の所有者](https://telegram.org/faq_spam)
- [2段階認証](https://core.telegram.org/api/srp)

### レンタルされた+888番号（Fragment）

一部のマーケットプレイスやサービスでは、Fragment を通じて Telegram の公式 +888 番号を一時的にレンタルできるサービスを提供しています。

おおよその価格：1日あたり20米ドルです。

- Telegram Web または Telegram Desktop で直接アカウントを登録することができます。
- 該当の番号でアカウントを削除し、新しいアカウントを作成しても構いません。
- これらのアカウントは一般的に不正防止チェックの対象となる頻度が低いですが、免責や特別な特権が与えられるわけではありません。

この番号はあなたのものではありません。レンタル期間が終了すると、所有者がその番号を取り戻すことができます。直ちにクラウドパスワードを設定し、このアカウントを長期的に使用するものとして扱わないでください。

ご自身で+888の番号を所有するか、ご自身が管理するプリペイドSIMカードを使用することが、より確実です。

### マーケットプレイスで販売されている既製アカウント

一部のマーケットプレイス（例えば G2G や Z2U など）では、新規、古くなったもの、またはセッションファイル付きの既製の Telegram アカウントが販売されています。

- [G2G：Telegramアカウントの掲載情報](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U：Telegramアカウント一覧](https://www.z2u.com/telegram/accounts-5-15140)

絶対にメインアカウントを使用しないでください！この方法で作成した専用アカウントであっても、メインのTelegramアカウントをTgWitnessに登録するよりも安全です。

#### 購入前の注意事項

- これはTelegramの利用規約に違反します。
- 多くのアカウントは一括登録（自動登録）されているか、または履歴が不明です。
- 一部の販売者には、依然として復旧用のアクセス権限が残っている場合があります。
- こうした市場からのアカウントは、後日、利用停止や制限を受けることが頻繁にあります。
- スティーラー、フィッシングツール、または明らかに盗まれたアカウントを公然と販売しているマーケットプレイスは避けてください。
- フィッシングツール、情報窃取ツール、盗まれたセッションやアカウントを公然と販売しているプラットフォームからアカウント（自動登録と宣伝されているものであっても）を購入することは、Telegramの利用規約に違反するだけでなく、ほとんどの国の法律にも違反します。これにより、後日、証拠が無効となる可能性があります。慎重に選択してください。

#### このオプションをご利用になる場合

1. このアカウントは使い捨てとして扱ってください。
2. その他のすべてのセッションを終了し、クラウドパスワードを設定し、直ちに復旧方法を変更してください。
3. 異なるプロバイダーのアカウント、またはご自身で登録したアカウントを2～3つご使用ください。

**プレミアム、削除、および7日間の猶予期間**

アカウントが「Premium」の場合、電話番号へのアクセス権を持つ人物であっても、そのアカウントを即座に削除することはできません。通知が届き、削除されるまでに7日間の猶予があります。

これは、あなたの調査が当該アカウントに依存しているため重要です。代替案を準備する時間はあります。

**新規アカウントおよびAPI認証情報**

SMSサービスから受け取った番号を使用してご自身で新規登録したアカウントから独自のapi_id/api_hashを取得・使用した場合、最初のAPIリクエストまたはセッション認証の際に、そのアカウントはログアウトされてしまいます。調査を計画する際は、この点にご留意ください。

04

## アカウントの作成

番号から、最初に記録されたチャットまで。

1. ### 番号を取得する

   アカウントを長期的に維持する必要がある場合はプリペイドSIMまたはeSIMを、短期的な作業の場合はレンタルまたは1回限りのアクティベーションをご利用ください。サービスの一覧は以下の通りです。
2. ### メインアカウントとは別に登録してください

   登録は、メインアカウントとは別のデバイス、エミュレーター、または電話プロファイル上の公式Telegramアプリで行ってください。
3. ### クラウドパスワードでロックしてください

   すぐに、他の場所では使用していないクラウドパスワードと復旧用メールアドレスを設定してください。
4. ### プライバシー設定を閉じる

   電話番号 「**誰もいない**」、「番号で私を検索」、「**私の連絡先**」、「最終アクセス日時」、「プロフィール写真」、「自己紹介」は、「**誰もいない」**または「**私の連絡先**」とし、連絡先の同期をオフにしてください。
5. ### 自己破壊を防ぐようにしてください

   アカウントの自動削除期間を最長に設定してください。そうすれば、TgWitnessの稼働を停止しても、アカウントを失うことはありません。
6. ### 中立的な印象を与えるようにしてください

   他のアカウントからの名前、写真、ユーザー名、プロフィール、および個人の連絡先は一切使用しないでください。
7. ### しばらく待機してください

   最初は1日に数件のチャットに参加するようにしてください。急いで参加しようとする新規アカウントは、最初に制限されます。
8. ### ボットとは一切情報を共有しないでください

   ボットに対しては、決して「電話番号を共有」や「位置情報を共有」を押さないでください。リンクやミニアプリは、そのデバイス上のVPNまたはプロキシ経由で開いてください。
9. ### TgWitnessに接続してください

   独自のワークスペースで、「**アカウント」→「QRコード」**から接続し、次に「**ソース」→「調査モード」**を押してください。アプリは操作を行う場所であり、TgWitnessは記録を保管する場所です。

Telegramのドキュメント

- [2段階認証](https://core.telegram.org/api/srp)
- [プライバシー設定](https://core.telegram.org/api/privacy)
- [アカウントの自動削除](https://core.telegram.org/method/account.setAccountTTL)

05

## サービス番号

開始時のオプションとして、国、価格、およびTelegramが電話番号の変更を頻繁に受け入れるかどうかを確認してください。お支払い前に必ずご確認ください。

### プリペイドSIMおよびeSIM 11

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
  - プリペイド

  PayGoプラン、非常に安価です
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - プリペイド
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - プリペイド
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - プリペイド
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### 仮想番号アプリ 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  米国限定；登録には米国の電話番号が必要です
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  その番号は、使用しない場合、取り消されます
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
  - その他の国
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
  - 有料

  試用期間中
- [Hushedhushed.com](https://hushed.com)

  - 多くの国では
  - 有料

  安価
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

  アプリ内の欧州の携帯電話番号
- [Sonetelsonetel.com](https://sonetel.com)

  - 多くの国では
  - フリーナンバー
- [Zadarmazadarma.com](https://zadarma.com)

  - 多くの国では

  仮想番号

### レンタルおよびアクティベーションの数 12

レンタルでは、番号が数週間または数ヶ月間有効です。1回限りのアクティベーションでは、1つのコードが発行されます。登録後すぐにクラウドパスワードを設定してください。

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - レンタル
  - 有効化
- [SMSPVAsmspva.com](https://smspva.com)

  - レンタル
  - 有効化
- [5SIM5sim.net](https://5sim.net)

  - レンタル
  - 有効化
- [SMSPoolsmspool.net](https://www.smspool.net)

  - レンタル
  - ワンタイム
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - レンタル
  - 有効化
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - レンタル
  - 有効化
- [JuicySMSjuicysms.com](https://juicysms.com)

  - レンタル
  - 有効化
- [365SMS365sms.org](https://365sms.org)

  - レンタル
  - 有効化
- [SIMSMSsimsms.org](https://simsms.org)

  - レンタル
  - 有効化
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - ワンタイム
- [SMS-MANsms-man.com](https://sms-man.com)

  - ワンタイム
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - ワンタイム
