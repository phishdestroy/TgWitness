# 独立した証人

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/witness/

独自の鍵とボットを使用してWitnessを実行し、署名済みのチェックポイントをチャンネルに公開し、エクスポートしたデータと照合してください。

[ロシア語によるボットとプロキシの設定方法](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md)。

コレクターは自身のジャーナルに署名するため、コレクターとその鍵を管理する者がいれば、 原則としてジャーナルを書き換えたり切り詰めたりして、再度署名することが可能です。 Witnessは、 その行為を検知可能にします。これは独立したプロセスであり、別のコンテナ、あるいはより正確には第三者が 運用するサーバーが、数分おきにコレクターの署名済みジャーナルの先頭部分を取得し、 確認した内容を自身の鍵で署名し、自身のジャーナルに保存した上で、Telegramチャンネルに投稿します。

フローチャート · コレクター → Witness (署名付きチェックポイント：記録数 + 先頭ハッシュ); Witness → Witnessジャーナル、独自の鍵; Witness → Telegramチャンネル (独自のボットを介して署名付きで投稿されました); 証拠 ZIP → verify.py; Witnessジャーナル、独自の鍵 → verify.py; Telegramチャンネル → verify.py (Telegram Desktopからのエクスポート、または「t.me/s」ページ) · コレクター · Witness · Witnessジャーナル、独自の鍵 · Telegramチャンネル · 証拠 ZIP · verify.py · 署名付きチェックポイント：記 · 録数 + 先頭ハッシュ · 独自のボットを介して署名付き · で投稿されました · Telegram · Desktopからのエクスポート、 · または「t.me/s」ページ

**図表をテキストで記述**

1. コレクター → Witness (署名付きチェックポイント：記録数 + 先頭ハッシュ)
2. Witness → Witnessジャーナル、独自の鍵
3. Witness → Telegramチャンネル (独自のボットを介して署名付きで投稿されました)
4. 証拠 ZIP → verify.py
5. Witnessジャーナル、独自の鍵 → verify.py
6. Telegramチャンネル → verify.py (Telegram Desktopからのエクスポート、または「t.me/s」ページ)

## TgWitnessが提供するもの、および提供しないもの

| Witnessには | このツールには決して |
| --- | --- |
| 1つのワークスペース用の読み取り専用**ウィットネストークン** | コレクターのTelegramセッションまたはAPI認証情報 |
| 独自のEd25519鍵とジャーナル | コレクターの保管庫、署名鍵、またはパネルトークン |
| 独自のTelegramボットトークン | メッセージの内容：ヘッダーには記録件数とハッシュ値が含まれます |

トークンは、パネルの「**Witness**」ページで生成され、一度だけ表示され、 SHA-256としてのみ保存されます。これにより、`GET /api/witness/head`というエンドポイントが正確に1つ開かれ、そこから 新たに署名されたチェックポイントに加え、署名済みのコンテンツを含まない収集カウンターおよび稼働状況が返されます。 このトークンでは、パネルを開いたり、メッセージの内容を読み取ったり、設定を変更したりすることはできず、 パネル側ではこのトークンは受け入れられません。トークンの無効化は同じページで行えます。コレクターは、 新しいウィットネスキーがチェックを開始した時刻（`witness.seen`）を記録し、トークンごとの最終チェック日時を表示します。 2.5インターバル以内にチェックが行われていないウィットネスは、期限切れとしてマークされます。

新しいウィットネスは、 各ポーリングごとにランダムなチャレンジを送信します。キャプチャステートメントは、コレクターの署名の下でそれを反映します。カウンターは 正確なチェックポイントに紐付けられており、署名付きウィットネス投稿に含まれます。レガシーヘッドは スタンドアロンのウィットネスによって引き続き受け入れられます。ジャーナルの増分のみは、決して新しいメッセージとしてカウントされることはありません。

## チェックおよび記録の対象

一定の間隔（デフォルトでは10分ごと）ごとに、witnessは以下の処理を行います：

1. ヘッド自体を取得します（コレクターはこれをプッシュしたりスキップしたりすることはできません）；
2. コレクターの署名、固定されたコレクターキー（`--collector-fingerprint`、 または最初に確認されたキー）、非減少のカウント、およびカウントが変更されていない状態でヘッドが変更されていないことを検証します。
3. 自身のジャーナルに署名付きレコードを追加します：`witness.anchor`（ステータス：`ok`、 `key_changed`、`rollback`（以前よりレコード数が少ない）、`fork`（長さは同じですが、 ヘッダーが異なる）、または`invalid`（検証に失敗した）、あるいは`witness.no_response`（ コレクターが応答しなかった場合））；
4. TgWitnessが 稼働中でBot APIにアクセス可能な間は、「no answer」を含め、署名付きの結果をチャンネルに投稿します。投稿ID（`witness.posted`）が記録され、 投稿に失敗した場合も同様に記録されます（`witness.post_failed`）。

投稿は次のような形式になります。最後の行には署名付きの記述が含まれています：

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## witnessを実行する

Telegramボット（@BotFatherで作成してください）、そのボットが 管理者となっているチャンネル、および証人からアクセス可能なコレクターのアドレス（プライベートネットワーク外で HTTPS経由）が必要となります（[導入手順の](https://phishdestroy.github.io/TgWitness/ja/docs/reference/deployment/)「HTTPSプロファイル」を参照してください）。

**[Extras] → [チャンネル内のボット] → [** パネルで**ボットを設定]** を選択してください。3つのステップで、 読み取り専用アクセス権、チャンネル、間隔の設定を行い、その後ウィットネスを起動します。公開 ポリシー、オプションのHTTP/SOCKS5プロキシ、およびカスタムBot APIアドレスは、**[詳細設定]** にあります。 このフォームから、 このワークスペースのコレクターキーが固定された`witness.json` をダウンロードします。「**アクセスファイルを**`witness-token.txt` として**保存** 」を選択して、新しく 作成された読み取り専用トークンをダウンロードし、そのJSONファイルの横に、ウィットネスホスト上で作成された`bot-token.txt` を配置してください。コレクターはボットトークンを受け取ることはありません。 ダウンロードを行っても、サービスの起動やメッセージの公開は行われません。ホスト型プロジェクトのウィットネスは、 暗黙的に登録されることはありません。

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

最初のコマンドは、ネットワークリクエストや鍵の 生成を行わずに、設定ファイルと秘密ファイルを確認します。JSON内のパスはそのファイルを基準とした相対パスであり、CLI/環境のパスは 作業ディレクトリを基準とした相対パスです。 ウィットネスのフィンガープリントは、ホストの外に保持してください。コレクターの 「last-poll」インジケーターはリクエストの確認のみを行います。公開については、Proof によって報告されるか、 ウィットネス・ジャーナルおよびチャンネルで確認してください。

パネルがSSHトンネルの背後に配置されている場合は、[このCaddyの例](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example)に従い、 別のHTTPSホスト名上で、スコープが限定されたwitnessエンドポイントのみを公開してください。 その場合、デフォルトのワークスペースでは`https://witness.example.org`が使用され、その他のワークスペースでは `https://witness.example.org/profiles/ID`が使用されます。トークンは引き続き必要となります。パネルおよびその その他のAPIルートは、その仮想ホストによって転送されません。

定期的にチェックポイントが公開される設定には「`all`」をお選びください。5分間隔の場合、ワークスペース1つあたり1日約288件の 投稿となります。「`changes`」および「`problems`」では、一部のチェックポイントを意図的に非公開としています。 MTProxyは、コレクター側のTelegramクライアント用です。WitnessのHTTPポーリングおよびTelegramのHTTPS Bot APIは、それぞれ独自のダイレクト/HTTP/SOCKS5ルート（[Bot API](https://core.telegram.org/bots/api)）を使用します。

**コレクターの隣に、Docker を使用して**（同じホスト上で — 独立したプロセスとキーですが、 オペレーターは同じです）：`.env` に値を入力し、プロファイルを起動してください。

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

掲載されている画像を使用する場合は、`docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d` をご使用ください。

**他者のサーバー**（真に独立した証人）**上で**：リポジトリをそこにコピーし、 `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` に上記の3つの値を `.env` に設定してから、

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

または、Docker を使用しない場合：

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### オプション

| オプション | 環境 | デフォルト | 意味 |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | チェック間隔（分）：1～1440 |
| `--timeout` | `_TIMEOUT` | 30 | コレクターおよびBot APIの応答待ち時間は数秒、5～600 |
| `--post` | `_POST` | `all` | `all`：すべてのチェック；`changes`：新たな課題または問題；`problems`：問題と未回答のみ |
| `--title` | `_TITLE` | `TgWitness witness` | 各チャンネルの投稿の冒頭部分 |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | 最初の回答を鵜呑みにするのではなく、コレクターキーを固定してください |
| `--proxy` | `_PROXY` | 直接 | `socks5://host:port` または `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Bot APIのアドレス（例：ローカルのBot APIサーバー） |
| `--data-dir` | `_DATA` | `witness-data` | Witnessキーとジャーナル |
| `--config` | `_CONFIG` | – | 上記のいずれかのオプションを含むJSONファイル |

コレクターアドレス、トークン、およびチャンネルは、`--collector`、`--token`、または `--token-file`、`--bot-token`、`--bot-token-file`、`--channel`、あるいは`_COLLECTOR`、`_TOKEN`、 `_TOKEN_FILE`、`_BOT_TOKEN`、`_BOT_TOKEN_FILE`、`_CHANNEL`から取得されます。これにより、機密情報が 処理リストに漏れるのを防ぎます。

設定ファイルでは、アンダースコア付きのオプション名に加え、`texts` を使用します。これは、 チャンネルの投稿文を置き換えるものです：

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts`キー：`ok`、`key_changed`、`rollback`、`fork`、`invalid`、`no_response`、`collector`、 `records`、`head`。コマンドラインは環境変数に優先し、環境変数はファイルに優先します。 未知のオプションやテキストキーは、無視されるのではなく、メッセージを表示してwitnessを停止させます。 記述内容は検証結果に影響を与えません。verify.pyは、各投稿の最後に署名付きトークンを チェックします。 `--post changes`または`problems`では、投稿されなかったチェックも引き続き ウィットネス・ジャーナルに残っており、`verify.py`ではそれらが「未投稿」として一覧表示されます。開始レコードには ポリシー名が記載されています。すべてのチェックは依然としてジャーナルに表示されるため、投稿回数が減っても、独立した Telegramの送信回数が減るだけで、チェックの数が減るわけではありません。

チャンネルがなくても、Witnessは引き続きジャーナルを保持します。Witnessのキーフィンガープリント （`python -m tgwitness.witness fingerprint`）は別の場所に保管してください。

## 検証

証人側では、そのジャーナルをエクスポートします：

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

その後、どこからでも、コレクターの署名付きZIPファイルと、Telegram Desktopからエクスポートしたチャンネル（*「チャット履歴のエクスポート」* →「JSON」を選択すると`result.json` が生成されます）またはその公開`https://t.me/s/…` ページを使用して：

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py`は、ウィットネス・ジャーナル（チェーンと署名）を確認した後、 **ウィットネスが検知したすべてのヘッドがエクスポートされたジャーナルに含まれているかを**検証します。つまり、そのカウントにおける記録には、 正確にそのハッシュが含まれている必要があります。一致しないヘッドがある場合、検証に失敗します。これは、 ウィットネスが検知した後、ジャーナルが変更されたことを意味します。 また、エクスポート後に確認されたヘッダー、証人が 記録した異常、検証に失敗した回答、この エクスポート内に一致するチェックポイントが存在する期間（「XからYまで証人確認済み」）、およびギャップについても報告します。それ以降のチェックポイントは、これらの期間を延長するものではありません。 結果には、最後に一致したレコード番号と、一致するチェックポイントのない 末尾のレコード数が含まれます。エクスポート自身の鍵で署名された回答のみがカウントされます。証人が 一度も確認したことのない鍵で署名されたエクスポートは「未確認」として報告され、`--fingerprint`がなければ、その 署名者は未固定のままとなります。 `--channel` では、署名されたすべての投稿が、証人ジャーナルと レコードごとに一致する必要があります。変更された投稿は検証に失敗し、欠落している投稿は一覧表示されます。提供された Telegram JSON エクスポート内の日付は、署名された証人トークンの範囲外にある編集可能なメタデータです。 トークンが一致しても公開日は認証されません。結果には、公開時刻の検証が 行われなかったことが明示的に報告されます。

### 証人付きエクスポートの境界が必要です

立会人の立会いのもとで作成された最終記録を含める必要がある引き継ぎの際は、`--require-witness`を追加してください：

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

これには、独立して保持されている「ウィットネス・フィンガープリント」と、このエクスポートの 正確な末尾にある一致するチェックポイントが必要です。より前のプレフィックスのみを カバーするチェックポイントでは不十分です。収集を一時停止し、ウィットネスに最終状態を 確認させた上で、ジャーナルへのさらなる書き込みが行われる前にエクスポートを行ってください。ジャーナルが変更された場合は、別のチェックポイントを保持し、 その状態をエクスポートしてください。 後のチェックポイントだけでは、より短いエクスポートの最終ハッシュを検証することはできません。 `--channel`も指定されている場合、主張された投稿の欠落や空のマッチセットは、この 厳格なチェックに失敗します。このフラグがない場合でも、通常の整合性チェックでは、 アーカイブ自体が破損していないにもかかわらず、証人による検証が行われていない レコードが報告されます。

このフラグは、提供され、固定された証言記録との整合性を確保するものです。運用者は 依然として、証言の独立性を確立し、その記録を別途保存する必要があります。 このフラグは、メッセージの真実性、完全な収集、または独立して測定された実行時間を保証するものではありません。

「ウィットネス」は、その時点でコレクターが報告した内容と、その後のエクスポート結果が それと一致していることを示します。コレクターがTelegramから配信されたすべてを記録したこと、あるいは メッセージの内容が真実であることを示すものではありません。同じオペレーターが同じマシン上で実行したウィットネスは、 他の誰かが実行したものよりも信頼性が低くなります。

単に件数が増加しただけでは、オンライン上の「追記専用」の連続性を立証することはできません。オフラインでの 比較において、保持されている各プレフィックスハッシュが、コレクターのエクスポートデータ全体と一致している必要があります。 Witnessのダウンタイムや公開の失敗により、外部のアンカーがない期間が生じます。欠落した 投稿は、保持されているWitnessジャーナルに対して報告することができます。同じ運営者が管理するチャンネルやサーバーは、 不変の第三者アーカイブとはみなされません。
