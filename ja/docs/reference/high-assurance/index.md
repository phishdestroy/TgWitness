# 高信頼性の導入

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/high-assurance/

Hetzner または Phala Cloud 上の 24 時間 365 日稼働のシールドサーバー、Gateway DNS、および第三者が再現可能な検証手順。

署名付きジャーナルは、**署**名**後に**記録が変更されていないことを証明します。深刻なケースでは、 次の疑問として、署名前に誰かがデータを改ざんした可能性がないかが挙げられます。 つまり、誰が、どのマシンでコレクターを実行したのか、また誰かがそこにログインしたかどうかです。このオプションの モードでは、オペレーターの主張ではなく、クラウドプロバイダーとCloudflareが保持する記録を用いて、 第三者がそれを確認できるよう、コレクターが展開されます。

通常のローカル環境およびDockerでの使用方法は変更ありません。 `python -m tgwitness.cloud`を使用してデプロイしない限り、ここで実行されるものはありません。また、コレクターはデプロイ設定で指定された場合にのみホストを読み取ります。 `TGWITNESS_ASSURANCE`.

フローチャート · オペレーター → サーバー、着信ルールなしのファイアウォール (プロバイダー API); オペレーター → トンネルとDNS (Cloudflare API); サーバー、着信ルールなしのファイアウォール → トンネルとDNS (送信専用); サーバー、着信ルールなしのファイアウォール → サーバー上で生成された署名鍵; Verifier、読み取り専用トークン → プロバイダーログとファイアウォール; Verifier、読み取り専用トークン → トンネルコネクタのアドレスとインジェス; Verifier、読み取り専用トークン → 署名済み /api/assurance ステートメント; Verifier、読み取り専用トークン → 証拠 ZIP · オペレーター · Verifier、読み取り専用トークン · サーバー、着信ルールなしのファイアウォール · プロバイダーログとファイアウォール · トンネルコネクタのアドレスとインジェス · 署名済み /api/assuranceステートメント · 証拠 ZIP · トンネルとDNS · サーバー上で生成された署名鍵 · プロバイダー API · Cloudflare API · 送信専用

**図表をテキストで記述**

1. オペレーター → サーバー、着信ルールなしのファイアウォール (プロバイダー API)
2. オペレーター → トンネルとDNS (Cloudflare API)
3. サーバー、着信ルールなしのファイアウォール → トンネルとDNS (送信専用)
4. サーバー、着信ルールなしのファイアウォール → サーバー上で生成された署名鍵
5. Verifier、読み取り専用トークン → プロバイダーログとファイアウォール
6. Verifier、読み取り専用トークン → トンネルコネクタのアドレスとインジェス
7. Verifier、読み取り専用トークン → 署名済み /api/assurance ステートメント
8. Verifier、読み取り専用トークン → 証拠 ZIP

## 検証者が確認できる内容

| 主張 | 検証方法 | 管理： |
| --- | --- | --- |
| このサーバーは、既知の時刻にプロバイダーのAPIを通じて作成されました。 | Serverオブジェクトと、プロバイダー独自のログにおけるその作成 | プロバイダー |
| プロバイダーのアクセスパスを使用したユーザーはいませんでした | コンソールリクエスト、レスキュー、パスワードリセット、再構築、ISO、イメージ、バックアップのログ | プロバイダー |
| 接続できませんでした | プロバイダのファイアウォールにはインバウンドルールがなく、SSHは初回起動時から非表示になっています。 | プロバイダー（ファイアウォール）、ホスト（SSH） |
| このパネルには、トンネルを経由してのみアクセスできます。 | Tunnelのイングレスはパネルのみへ転送され、コネクタはサーバーのアドレスから実行されます。 | Cloudflare |
| このソフトウェアは、 | コレクターの署名付きソースツリーのハッシュ値は、デプロイされたコミットのチェックアウトと一致します。 | Collector、Git との照合済み |
| 署名鍵はそのサーバー上で作成されました | この鍵は、プロバイダのサーバーIDと、受信したcloud-initのハッシュ名を記載したステートメントに署名します。 | Collector：プロバイダーとの照合済み |
| このジャーナルは、そのキーおよびサーバーに属しています | 証拠ZIP内のすべてのプロセス開始には、そのサーバーのホスト測定値が含まれています。 | 証拠 ZIP |

ホストの測定値（SSHリスナーおよびプロセス、現在のセッション、 `wtmp`、起動） はコレクター自体によって報告され、プロセスの起動時および `host.state` 変更があるたびに記録に署名されます。サーバーのroot権限を持つユーザーはこれらを改ざんする可能性がありますが、 これらはプロバイダーやCloudflareの記録に取って代わるものではなく、それらを補完するものです。

## プロバイダー

| `--provider` | 認証情報 | Verifierの読み取り専用アクセス権 | 検証者向けのプロバイダーログ | 保存目的： |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | 同じプロジェクトのリードトークン | サーバーおよびファイアウォールの動作 | リソースが存在する限り |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | 読み取り専用の個人アクセストークン | Dropletのアクション | Dropletが存在している間は |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` 読み取り専用スコープ | アカウントのイベント、ファイアウォールルールのバージョン | 90日間 |
| `vultr` | `VULTR_API_KEY` | 読み取りアクセス権を持つユーザーおよび `activity_logs` 権限 | アカウントのアクティビティログ（メソッド、パス、アクター） | 30日間。監査ログのサブスクリプションを利用すれば、さらに長期に保存可能です。 |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrailのイベント履歴 | 90日間 |
| `phala` | `PHALA_CLOUD_API_KEY` | 同じワークスペースのAPIキー | アプリケーションの更新：構成および環境の変更、再起動、OSのアップグレード | このアプリケーションが存在する限り |
| `generic` | なし | なし | なし：**自己認証済み** | – |

各ケースごとに専用のプロジェクト、チーム、アカウント、またはサブアカウントを使用してください。これにより、検証者の 読み取り専用アクセス権では、このデプロイメントのみが表示されます。認証情報は `--provider-token-file` または上記の変数から読み込まれ、コマンドラインからは決して読み込まれません。AWSの場合、ファイルには 地域が格納されます `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; リージョンは `--location`.

各プロバイダーの記録には含まれない情報が、すべてのレポートに記載されています。 要約すると：Hetznerは コンソールへのリクエストをログに記録します。一方、DigitalOceanのRecovery Console、LinodeのLish/Glish、およびVultrのWeb コンソールは、そのものとしてはログに記録されません。そのため、初回起動時にはrootがロックされ、コンソールにログインするには パスワードのリセットまたはブート方法の変更が必要となりますが、これらはログに記録されます。Vultrは、インスタンスを読み取れるキーに対してコンソールの アドレスを返しますが、記録にもレポートにもそのアドレスは保存されません。

## Phala Cloud上の機密VM（Intel TDX）

この `--provider phala` コレクターは、dstackによって管理[されるPhala Cloud](https://phala.com/)上の Intel TDX機密仮想マシン内で実行されます。ホストおよびPhalaのスタッフは、その メモリを読み取ることができず、プロセッサはマシンが起動した内容に関する証明に署名します。検証者は Phalaの主張を鵜呑みにしません： `tgwitness.tdx` すべての証明を、ピン留めされたIntel SGXルートCAに至るまで、Intelの失効リストおよびIntelが署名したプラットフォームデータと照合して自ら検証し、デバッグや移行が可能な マシンは拒否します。

| レポートの登録 | 表示内容 |
| --- | --- |
| `tdx_binding` | この認証には、コレクターによる署名付き声明およびこのリクエストのランダム値が含まれます。 |
| `tdx_quote` | Intel はこの認証を保証しており、Intel がプラットフォームを最新の状態であると評価した場合にのみ、認証に合格します。 |
| `tdx_compose_hash` | dstack イベントログから再生される RTMR3 は、コレクターが報告するアプリ作成の状況を測定します。 |
| `tdx_compose` | そのコンパイル結果は、デプロイされたコミットのコードが生成するものとバイト単位で完全に一致しています。ソースファイルはハッシュで、両方の画像はダイジェストで固定されており、その他のコードは一切含まれていません。 |
| `tdx_identity` | 認証情報は、デプロイされたアプリケーションおよびインスタンスから提供され、PhalaのKMSからの鍵と暗号化されたディスクが使用されます。 |
| `tdx_os` | ここで `--tdx-measurements`、MRTD および RTMR0-2 は、dstack OS イメージから計算された値と等しくなります（`dstack-mr measure --json`) |

ジャーナルに記録されたコレクターの起動のたびに、このような証明が付与されるため、 `verify --evidence` 各起動を検証します。Phalaのアプリケーションリビジョン一覧が プロバイダーログとして機能します。デプロイ後にコンポーズが変更された場合、レポートは失敗します。

パネルで、「**Extras** 」→「**Server 24/7** 」の下にある「**Confidential virtual machine · Phala Cloud** 」を選択し、Phala CloudのAPIキーを貼り付けてください。クイックトンネルはHetznerと同様に機能します。コマンドラインからは次のように実行します：

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --tdx-measurements dstack-mr.json
```

`--tdx-collateral` Intelの証明書および失効リストを、Intelからダウンロードする代わりに ファイルから読み込みます。ここではGateway DNSは利用できません。Phalaには、 送信トラフィック用のプロバイダファイアウォールがないためです。

この証明によって、IntelのTDXモジュールやマイクロコードの欠陥、あるいはメモリバスへの物理的なアクセスを 完全に排除できるわけではありません。Phalaのアカウント内のアプリケーションを制御している者は、別のコンポーズを展開することができ、 それは新しいコンポーズハッシュを持つ新しいリビジョンとして表示されます。ホストは、マシンの時刻 ソースとネットワークを制御しています。

## 始める前に

1. Cloudflareゾーン、そのアカウントID、**およびCloudflare Tunnelの編集**、 **ゾーンの読み取り**、**DNS編集**が可能なAPIトークン。これらは `--cloudflare-token-file` または `CLOUDFLARE_API_TOKEN`で指定されます。検証者向けには、**Cloudflare Tunnelの読み取り権限**、**DNSの読み取り権限**、および 監査ログ用のアカウント設定の**読み取り権限**が必要です。ドメインがない場合、 [クイックトンネル](https://phishdestroy.github.io/TgWitness/ja/docs/reference/high-assurance/#quick-tunnel-without-a-domain)ではこれらはいずれも不要です。
2. 専用プロジェクトへの書き込み権限を持つプロバイダーの認証情報； `lock` 以下も同様に使用します：

   - Hetzner：読み取りおよび書き込み権限を持つAPIトークン；
   - DigitalOcean：書き込み権限付きの個人用アクセストークン；
   - Linode： `linodes`, `firewall` および `events` 読み取り/書き込みスコープを持つ個人用アクセストークン；
   - Vultr：専用アカウントまたはサブアカウントのAPIキー；
   - AWS：IAM 認証情報の使用が許可されています `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` および `ec2:RevokeSecurityGroupIngress`.
3. 実行するコミット。リリースタグは、 `git ls-remote`; サーバーが受け取るのは、常に40文字のコミットのみです。

## パネルから

ご自身のコンピュータで、「**Extras」→「Server 24/7」**を実行すると、 `deploy` Hetzner用サーバーを3つの 手順で実行します：ヨーロッパまたは米国を選択し、Hetznerトークン（読み取り・書き込み）を貼り付け、その後、 そのトークンでパネルが検出したサーバータイプ、月額料金、アドレス、バージョンを確認します。確認するまでは 何も作成されません。パネルには各手順が `deploy` 表示し、その後、 アドレス、パネルトークン、および署名キーのフィンガープリントが表示されます。ドメインがない場合、サーバーには [クイックトンネル](https://phishdestroy.github.io/TgWitness/ja/docs/reference/high-assurance/#quick-tunnel-without-a-domain) が設定されます。**「Your servers」→「Find the current address」では** 、再起動後に再度アドレスが検索されます。独自のドメインで固定アドレスを設定するには、 **「Optional」→「your own domain」** を開き、Cloudflareトークンを追加します（準備済みのリンクでは、「Zone Read」、「DNS Edit」、および「Cloudflare Tunnel Edit」が選択されます）。

トークンは、ブラウザのタブから同じコンピュータ上のTgWitnessへ、各リクエストごとに転送され、 どこにも書き込まれません。デプロイメント記録、編集済みのcloud-init、パネルトークン、および クイックトンネル用のアドレスキーは、 `deployments/NAME` データディレクトリ内に保持されます。 パネルは、直接のループバック接続（ （`127.0.0.1`、プロキシやトンネルヘッダーなし）。ネットワーク経由でアクセスされたパネルでは、代わりにコマンドが表示されます。 バージョンは、GitHub APIを通じて解決される、実行中のパネルのリリースタグがデフォルトとなります。 場所、サーバータイプ、価格はHetznerのAPIから取得されます： `cpx22` 提供されている場合はそちらが使用され、 そうでない場合は、メモリが2 GB以上の最も安価なx86タイプが使用されます。

## ドメイン不要のクイックトンネル

`--quick-tunnel` 置き換える `--zone`, `--cloudflare-account` および `--panel-host`; Cloudflareの アカウントやトークンは一切使用されません：

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

サーバー上では、cloudflaredがパネルへの [クイックトンネル](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/)を開きます。 これは、Cloudflare経由で `https://….trycloudflare.com` アドレスで、cloudflared またはサーバーが再起動するたびに変更されます。サーバー上の小さなサービスが、各アドレスをランダムな ntfy.sh トピックに投稿し、デプロイメントディレクトリにのみ保持されている鍵で （`address-key.txt`）、そしてntfy.shが投稿を12時間保持するため、3時間ごとにこれを繰り返します。 `deploy` および**「現在のアドレスを検索」**は署名付き投稿のみを受け付けるため、偽造された投稿によって あなたやあなたのパネルトークンが他人のアドレスに転送されることはありません。トピックは記録に残り、 公開された cloud-init にも記載されます。これらを保有する者なら誰でも現在のアドレスを読み取ることができますが、その際も依然として パネルトークンの入力が求められます。いずれの場合も、サーバーは受信ポートを一切開放しません。

費用について：Cloudflareアカウントがないとクイックトンネルの記録が残らないため、 `verify` 、 トンネル、コネクタ、DNSチェックは利用不可と報告され、結果はせいぜい `incomplete`となります； プロバイダーの記録、ファイアウォール、署名付きステートメント、ホスト測定、およびインストーラーの比較は 通常通りチェックされます。参照用インストーラーとのバイト単位の比較には、 既に `--quick-tunnel`。0.7.0のチェックアウトではドメインインストーラーがビルドされ、 差異が報告されます。 Cloudflareはクイックトンネルに対して稼働時間の保証を行わず、処理中のリクエストは200件までしか許可せず、 Server-Sent Eventsも伝送しないため、パネルのライブ更新（バージョン0.7.0以降）が クイックトンネル経由で届かない可能性があり、ビューを再読み込みする必要がある。この点については未検証である。 確実に動作させる必要がある場合は、独自のドメインを使用すること。

## デプロイ

送信されるすべての内容を事前に確認してください。 `plan` プロバイダーやCloudflareへのリクエストは一切行いません：

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

その後、同じオプションと認証情報を使用してデプロイします：

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

最初に利用すべきサーバーの種類： `cpx22` (Hetzner)、 `s-1vcpu-2gb` (DigitalOcean)、 `g6-standard-1` (Linode)、 `vc2-1c-2gb` (Vultr)、 `t3.small` (AWS)。 `--location` および `--image` 各 プロバイダーの欧州リージョンにあるUbuntu 24.04をデフォルトとして設定します。

`--repository` 別の https Git リポジトリからのコミットを取得します。この際、URL に認証情報は含まれません （デフォルトでは `https://github.com/phishdestroy/TgWitness.git`). `deploy` は `--out` 別のデプロイディレクトリも受け付けます（デフォルト `deployments/NAME`; すでに デプロイが含まれているディレクトリは拒否されます）と、 `--wait`、コレクターの署名付きステートメントを待つ時間（分）： 1～240、デフォルトは20、または60（ `generic`.

コマンド：

1. Cloudflareトンネルを作成し、そのインジェストはパネルのホスト名をパネルへ転送し、 指定されている場合は、ウィットネスのホスト名を `/api/witness/head` および `/api/assurance` のみへ転送するCloudflareトンネルを作成します。
2. それらのホスト名に対してプロキシ化されたCNAMEレコードを作成し、既に存在する名前は拒否します。
3. 着信ルールのないプロバイダーファイアウォールと、その背後にSSHキーなし、 バックアップなし、コンソールエージェントなし、かつSSHを隠蔽し、rootをロックし、 `cloudflared`、正確にそのコミットを取得し、検証した上で、TgWitnessを 強化されたsystemdサービスとして起動します；
4. コレクターからの署名付きステートメントを待ち受け、そのステートメントにこのサーバーと この cloud-init のハッシュが指定されていることを確認します。

`deployments/case-2026-11/` 以下のように記述します：

| ファイル | 目次 | 共有しますか？ |
| --- | --- | --- |
| `deployment.json` | ID、ハッシュ、実行されたAPI呼び出し（メソッド、パス、ステータス）、および最初に署名されたステートメント | はい、検証ツールを使用します |
| `cloud-init.redacted.yaml` | 2つのシークレットが置き換えられた正確な cloud-init は以下の通りです。 `REDACTED` | はい |
| `panel-token.txt` | パネルトークン | いいえ |

プロバイダーのルートパスワード、トンネルトークン、パネルトークンは、決して `deployment.json`。末尾に表示されるコレクターのフィンガープリントは、 自身が単独で管理していないチャネル（例えば、ウィットネスチャネルや受信者へのメッセージなど）を通じて公開してください。

Telegramには、 `https://case.example.org` で、 [アカウント](https://phishdestroy.github.io/TgWitness/ja/docs/reference/accounts/)ガイドに記載されているように、パネルトークンを使用してTelegramにログインしてください。パネルの操作は署名付きジャーナルに記録されますが、これらは SSHセッションではありません。[ウィットネス](https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/)はポーリングを行うことができます `https://case-witness.example.org`.

SSH 機能はありません。ブートストラップに失敗した場合、コレクターは一切応答しません。サーバーを削除して 再デプロイするか、デバッグデプロイを使用して原因を特定してください。

### ユーザーデータに含まれる秘密情報

cloud-initには、パネルトークンとCloudflareトンネルトークンの2つのシークレットが含まれています。 署名鍵はこれらには含まれておらず、サーバー上で生成されます。Hetzner、DigitalOcean、Linodeは APIを通じてユーザーデータを返しません。Vultrは、インスタンスを読み取れる任意のキーに対して データを返し、EC2は `DescribeInstanceAttribute`。AWSの場合は、検証者に表にある3つの アクションのみを許可し、決して `ec2:Describe*`。Vultr については、検証者のキーが両方の トークンを読み取れるものと仮定します。トンネル・トークンがあれば、誰かが 2 つ目のコネクタを実行できます： `verify` サーバー上にないコネクタを すべて報告し、コレクターのステートメントは、それぞれが 新しいチャレンジに署名するため、その方法では偽造できません。 `--quick-tunnel` 2つ目のシークレットは代わりにアドレスキーとなります： これを読み取った者は、パネルが受け入れる偽のアドレスを投稿することができます。

収集担当者の公式声明には、サーバーのアドレスやログイン元の情報は記載されていませんが、 これらはいずれも署名付きジャーナルに記録されています。

## デバッグ展開とロック

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` 1つのアドレスまたは小規模なネットワーク（IPv4の場合は最大/24、IPv6の場合は最大/48）からの1つの鍵に対してSSHを維持します。 `KEY` すでにプロバイダーに登録済みであること： Hetznerプロジェクト内のSSHキーの名前またはID、DigitalOceanチーム内の SSHキーのIDまたはフィンガープリント、プロファイルのSSHキーがrootに追加されているLinodeのユーザー名、 Vultrアカウント内のSSHキーのID、またはリージョン内のEC2キーペアの名前。これらの オプションは `generic`には適用されません。このようなデプロイは `debug` として記録され、**決して** 高保証として報告されることはありません。作業が完了したら、 `sudo tgwitness-lock` を最後の SSH セッションの最後のコマンドとして実行し、その後：

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

ファイアウォールはすべてのインバウンドルールを無効にします。その後、レポートにはSSHが許可されていた時期と 遮断されていた時期が表示され、そのウィンドウは表示されたままになります。

## デプロイメントを削除する

`destroy` デプロイメントのラベルに基づいてサーバーとそのファイアウォールを削除し、 途中で失敗したデプロイメントも同様に削除した後、その トンネルを指すDNSレコードとトンネル自体を削除します。サーバーのジャーナルと署名鍵も同時に削除されます。その前に、 証拠をエクスポートしてください。記録は残され、 `removed`、削除処理のAPI呼び出しが記録されます。

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Hetznerについては、API経由での削除機能が実装されています。その他のプロバイダーの場合 `destroy` は、何かを削除する前に 停止し、プロバイダーのコンソールで削除するラベルを指定します。手動でインストールされた サーバー（`generic`）は、トンネルとDNSレコードのみが失われます。クイックトンネルの展開には Cloudflareトークンは不要です。そのトンネルはサーバーで終了し、投稿はntfy.shから 12時間以内に失効します。

## 任意のサーバー（自己認証型）

`--provider generic` これは、購入または手動でインストールしたサーバー向けです。 `deploy` トンネル とDNSを作成し、 `install.sh` （プライベート）および `install.redacted.sh` （公開用）を書き込み、待機します。 このファイルを `install.sh` を新しくインストールした Ubuntu 24.04 サーバーにコピーし、そこで実行してください：

```
sudo bash install.sh
```

このツールは、ホストの状態（ログイン情報、アカウント、 `authorized_keys`、リスニングソケット、 サービス、スケジュールされたジョブ、パッケージ）を記録し、コミットをインストールし、ホストのファイアウォールを有効化し、 自身を削除し、SSHをマスキングしてセッションを終了します。このようなサーバーに関するレポートは、せいぜい **「自己証明型（SELF-ATTESTED）」**です。つまり、インストーラを実行した人物はそれ以前にroot権限を持っており、検証者にはプロバイダーの記録が 利用できません。とはいえ、説明のつかないサーバーよりはましです。インベントリ、 インストーラのハッシュ、およびその後のすべてのログインには署名が付いています。

## 検証

検証者には `deployment.json`、公開されているインストーラー、読み取り専用の認証情報、そして 理想的には、そのコミットのチェックアウトと証拠ZIPが必要です：

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

すべてのプロバイダーおよびCloudflareの値は、その時点で検証者によって要求されます。記録には、 照会対象となるIDのみが含まれます。終了コードは、**PASS**の場合は0、**FAIL**の場合は1、 **REVIEW**、**INCOMPLETE**、**またはSELF-ATTESTED**の場合は2となります。 `--fingerprint` は独立した チャンネルから送信される必要があります。それがなければ、キーはオペレーターの記録とのみ照合されます。 `python verify.py` [Evidence](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/) と同様に、ZIPの証拠自体を検証します。

プロバイダーのアクションは分類されます。作成および作成後30分以内の起動は合格となります。 コンソール、レスキュー、パスワードリセット、再構築、ISO、イメージ、スナップショット、バックアップ、Systems Manager、 EC2 Instance Connect、およびファイアウォールの開放は不合格となります。電源関連のアクションや予期されない動作は すべてレビュー対象としてマークされます。未知のアクションが黙って通過することは決してありません。

## 証拠の引き渡しに関する報告書

`--report report.md` Markdown形式のレポートを作成し、 `report.json` その横に：

1. 結果、コレクターキーのフィンガープリント、デプロイ、プロバイダー、コミット、サーバー、ファイアウォール、トンネル；
2. 各チェックとそのステータス、およびソース（プロバイダーAPI、Cloudflare API、コレクターのステートメント、 証拠ジャーナル）；
3. 各アクションの評価、およびプロバイダーが記録している場合はその実行者を記載したプロバイダーログ；
4. トンネルの接続、設定、監査ログを保持する Cloudflare エンドポイント；
5. 署名済みの収集者声明；
6. 本レポートが明らかにしている点と、明らかにしていない点；
7. 再現するためのコマンド、および渡されたすべてのファイルのSHA-256。

レポート、 `report.json`, `deployment.json`、公開済みのインストーラー、および 証拠ZIPを提出してください。レポートは早めに作成してください。プロバイダーのログは一定期間しか保存されません。

## 外部ウィットネスとしてのCloudflare

ここにある機能はすべてオプションです。Cloudflareアカウントがなくてもサーバーは動作し、 現在、以下の2つの機能が利用可能です：

| 概要 | 表示内容 | TgWitness内 |
| --- | --- | --- |
| クイックトンネルまたは独自のドメインのトンネル | このパネルには、トンネルを経由してのみアクセスできます | サーバーウィザードについては、上記を参照してください |
| drand リレー `drand.cloudflare.com` | drandラウンド後の記録はそれよりも新しいものです。このジャーナルは、その都度書き綴られていきました。 | 証拠モード、**追加の証人**、アカウントなし（[フォーマット](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)） |
| トンネルの状態に関する通知 | トンネルがダウンした際、CloudflareからのメールまたはWebhookによって通知されます | Cloudflareダッシュボードで設定してください |
| ウィザードで「Gateway DNS (`--gateway-dns`、またはウィザード内の「**Cloudflare Gateway DNS**」） | サーバーが検索したすべての名前に対して、CloudflareがTLS経由で応答しました。Hetznerのファイアウォールにより、DNSはそれ以外のどこにも到達できません。ゲートウェイポリシーによって応答を書き換えることができたかどうか | Hetzner、無料のゼロトラストプラン、ドメインなし； `verify` ファイアウォール、ロケーション、ロギング、ポリシー、サーバーのクエリ、監査ログを確認します。エビデンスモードでは、ログがジャーナルにコピーされます。 |
| Cloudflareとのゲートウェイ：サーバー上の1つのクライアント、Cloudflareのみを通すアウトバウンドファイアウォール | DNSだけでなく、サーバーが行ったすべての接続 | まだ実装されていません |
| パネルの前面からのアクセス | パネルに誰がいつログインしたか | 未実装：独自のドメインが必要です |
| SSH コマンドのログ記録 | デバッグセッション内の各コマンド | まだ実装されていません |

Cloudflare独自のコピーをR2に保存する「Logpush」はエンタープライズ機能です。無料 プランでは、Cloudflareは `logpush is not enabled for this account`。ゲートウェイのログはそこで24 時間保持されるため、エビデンスモードでは、それが署名付きジャーナル（**Cloudflare Gatewayによる このサーバーのDNSクエリのログで**、「Account Analytics Read」権限を持つ読み取り専用トークン）にコピーされます。

ゼロトラスト計画がない場合、アカウントには1つのDNSロケーションがあります。Cloudflareが別のロケーションを拒否すると、 サーバーは既存のロケーションを共有し、そのクエリはアドレスによって区別されます。このフィルタには ゼロトラストPII読み取り権限も必要であり、 `destroy` 共有ロケーションが残ってしまいます。1つのログクエリは 最大3時間にわたるため、コピーと `verify` 3時間ごとのウィンドウでその日のデータを読み取ります。

Gateway DNSはシステムリゾルバをカバーします。ポート443経由で別のリゾルバへのDNS over HTTPSや、 どこにも解決されないアドレス（Telegramのデータセンターなど）への接続は、 そのログには記録されません。

Cloudflareは、Telegramの暗号化内部、Telegramアカウントに紐づく他のデバイス （エビデンスモードのデバイスリストはTelegram側からそれらを記録します）、およびプロバイダーのハイパーバイザーを閲覧することはできません。

2026年11月1日、Gateway DNSは実際のHetzner Cloudおよび無料のCloudflareアカウントに対して動作しました： Hetznerはアウトバウンドルールを承認し、サーバーにはv0.7.0がインストールされ、すべてのルックアップは TLS経由でGatewayを経由し、クイックトンネルはそのファイアウォールを通過し、 `verify` Cloudflareから サーバーの19個のホスト名（UbuntuおよびHetznerのミラー、GitHub、PyPI、NTP、 トンネル、ntfy.sh）を読み取りました。パネルは8つのウィンドウで36件のクエリをジャーナルに記録し、 `verify.py` それらを漏れなく要約し、 `destroy` サーバーとファイアウォールを撤去し、 共有場所を後にした。

## これによって確立されないこと

- プロバイダーとそのスタッフは、ハイパーバイザー、ディスク、ネットワークを管理します。
- ホストの測定値は、コレクターによって自己申告されます。
- 以前のファイアウォールルールの内容は、すべてのプロバイダーのログに記録されているわけではありません。Linodeのみがルールのバージョンを保持しています。
- メッセージの真正性については特に新しいことは述べていません。「[証拠」](https://phishdestroy.github.io/TgWitness/ja/docs/reference/evidence/)を参照してください。

## こちらでテスト済み

デプロイ、ロック、検証のロジックは、公開されているAPIリファレンスに基づいて構築された、 Hetzner、DigitalOcean、Linode、Vultr、EC2/CloudTrail、Cloudflareの各APIをシミュレートした環境に対する自動テスト、 およびAWSが公開している例に基づいたAWSリクエストの署名によって検証されています。 `tools/check_cloud_wizard.py` パネルのサーバーウィザードも同様に、ドメインと クイックトンネルを使用して実行されます。 `tools/check_tdx.py` dcap-qvlおよびdstackから、Intelのルート証明書に至るまでの 実際のIntel TDXアテステーションを検証します（ソース[はtools/tdx/README.md](https://github.com/phishdestroy/TgWitness/blob/main/tools/tdx/README.md)にあります）； `tools/check_phala.py`シミュレートされたPhala Cloudに対して、デプロイ、検証、ジャーナル、破棄、およびパネルウィザードを実行します。 このPhala Cloudの認証情報は、IntelのPKIを模倣して偽造されたPKIから得られています。Phala Cloud自体でのPhalaパスは、 まだ試されていません。

2026年11月1日、クイックトンネルパスは、パネルおよびコードから、**実際のHetzner Cloud**（ニュルンベルク、 `cpx22`、 TgWitness v0.7.0）、実際の ntfy.sh および GitHub に対して、コントロールパネルおよびコードから実行されました：

- 価格の確認後、パネルのボタンから作成を行います。13秒後にサーバーが稼働し、 約2分後には、インスタンスとインストーラーのハッシュが一致した署名付きステートメントが生成されます。
- trycloudflare.com のアドレスから開かれたサーバー独自のパネルで、 パネルトークンが受け入れられました。トークンがない場合は 401 を返します。
- Hetzner API 経由で再起動した後、サーバーは新しい署名付きアドレスを公開しました。 **現在のアドレス**を見つけましたが、古いアドレスは応答しなくなり、署名鍵は 変更されませんでした。ntfy.sh のトピックへの署名なしの投稿は無視されました。
- `verify` HetznerのAPIに対する検証：サーバー、着信ルールなしのファイアウォール、ステートメント、バインディング、 ホスト測定、ブート、およびv0.7.0チェックアウトのソースハッシュが合格しました。Cloudflareの 検証は、前述の通り利用できませんでした。インストーラーはv0.7.0がビルドするものと異なり、 このバージョンのコードがビルドするものとバイト単位で一致しました。
- パネルからの削除により、デプロイメントで指定されたサーバーとファイアウォールのみが正確に削除されました。 同じプロジェクト内の他のサーバーやファイアウォールには影響がありませんでした。

実際のアカウントではまだ実行されていません：独自のドメイン（Cloudflareトンネルおよび DNS）でのデプロイ、その他のプロバイダー、デバッグ用デプロイ、 `lock`、そのようなサーバー上のTelegramアカウント、 およびクイックトンネルを介した後続バージョンのライブ更新。各プロバイダーでの最初のデプロイを 以下で確認してください `plan`、デバッグ用デプロイメント、および `verify` 、クイックトンネルを介した後続バージョンのライブ更新を確認してください。ケースでこれを利用する前に、各プロバイダーでの最初のデプロイメントを、デバッグ用デプロイメント、および
